const express = require('express');
const axios = require('axios');
const router = express.Router();

router.get('/:specialist', async (req, res) => {
  const specialist = req.params.specialist;
  const city = "Chennai";
  const apiKey = process.env.GOOGLE_MAPS_API_KEY;

  try {
    const response = await axios.get(`https://maps.googleapis.com/maps/api/place/textsearch/json`, {
      params: {
        query: `${specialist} in ${city}`,
        key: apiKey,
      },
    });

    const results = response.data.results.slice(0, 3).map(doc => ({
      name: doc.name,
      address: doc.formatted_address,
      rating: doc.rating,
      mapsLink: `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(doc.name + " " + doc.formatted_address)}`
    }));

    res.status(200).json(results);
  } catch (err) {
    res.status(500).json({ error: 'Failed to fetch doctors' });
  }
});

module.exports = router;
