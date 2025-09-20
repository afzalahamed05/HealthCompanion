const admin = require('firebase-admin');

// Middleware to protect routes
const verifyToken = async (req, res, next) => {
  try {
    const header = req.headers.authorization;

    // Check if token exists and has the proper "Bearer <token>" format
    if (!header || !header.startsWith('Bearer ')) {
      return res.status(401).json({ message: 'No token provided or invalid format' });
    }

    // Extract the token string
    const token = header.split(' ')[1]; // Splits into ["Bearer", "<token>"]

    // Verify Firebase token using Admin SDK
    const decodedToken = await admin.auth().verifyIdToken(token);

    // Attach decoded user info to the request object for use in routes
    req.user = decodedToken;
    console.log("Auth Header:", req.headers.authorization);
    // Move to next middleware or controller
    next();
  } catch (error) {
    console.error('Token verification failed:', error.message);
    res.status(401).json({ message: 'Unauthorized: Invalid or expired token' });
  }
};

module.exports = verifyToken;
