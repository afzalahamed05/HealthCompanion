const express = require('express');
const router = express.Router();

// Save user data
router.post('/register', async (req, res) => {
  const db = req.app.get('db');
  const { uid, name, age, phone, email, username } = req.body;

  try {
    await db.collection('users').doc(uid).set({
      name,
      age,
      phone,
      email,
      username,
      createdAt: new Date()
    });
    res.status(200).json({ message: 'User profile saved successfully' });
  } catch (err) {
    res.status(500).json({ error: 'Failed to save user profile' });
  }
});

// Get user data
router.get('/:uid', async (req, res) => {
  const db = req.app.get('db');
  try {
    const doc = await db.collection('users').doc(req.params.uid).get();
    if (!doc.exists) {
      return res.status(404).json({ error: 'User not found' });
    }
    res.status(200).json(doc.data());
  } catch (err) {
    res.status(500).json({ error: 'Error retrieving user data' });
  }
});

module.exports = router;
