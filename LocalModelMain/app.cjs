const https = require('https');
const fs = require('fs');
const express = require('express'); // or any other framework
const path = require('path');

const app = express();

// SSL options
const options = {
  key: fs.readFileSync('server.key'),
  cert: fs.readFileSync('server.cert')
};

// Serve static files from the "public" directory
app.use(express.static(path.join(__dirname, 'public')));

// Serve the HTML file at the root route
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

const PORT = process.env.PORT || 3000;
const HOST = '10.1.7.160';

https.createServer(options, app).listen(PORT, HOST, () => {
  console.log(`Server started on https://${HOST}:${PORT}`);
});

