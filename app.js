import express from "express";
import path from "path";
import multer from "multer";
import { PreciseResponse } from "./openai-test.js";
import { fileURLToPath } from 'url';
import fs from 'fs';
import https from 'https';

const app = express();
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const options = {
    key: fs.readFileSync('server.key'),
    cert: fs.readFileSync('server.cert')
};

app.set("port", process.env.PORT || 3000);
app.set("views", path.join(__dirname, "views"));
app.set("view engine", "ejs");

app.use(express.static(path.join(__dirname, 'public')));
app.use(express.urlencoded({ limit: '10mb', extended: true }));

app.get('/', (req, res) => {
    res.render('index');
});

const PORT = process.env.PORT || 3000;
const HOST = '10.1.7.160';

https.createServer(options, app).listen(PORT, HOST, () => {
    console.log(`Server started on https://${HOST}:${PORT}`);
});

// Configure multer for handling file uploads
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
      cb(null, 'public/uploads/'); // Ensure 'public/uploads' directory exists
    },
    filename: function (req, file, cb) {
      cb(null, Date.now() + path.extname(file.originalname)); // Ensure unique filenames
    },
 });
  

const upload = multer({ storage: storage });

app.get('/', (req, res) => {        //NEW
    res.render('index');
  });

// Route to handle file upload and processing
app.post('/upload', upload.single('image'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).send('No files were uploaded.');
    }

    const imageUrl = `public/uploads/${req.file.filename}`; // Adjust based on your file storage

    // Process image using OpenAI API
    const result = await PreciseResponse(imageUrl);

    // Render 'result.ejs' with the result data
    res.render('result', { imageUrl, result });
  } catch (error) {
    console.error("Error processing image:", error);
    res.status(500).send('Error processing image.');
  }
});


app.post('/upload-photo', async (req, res) => {
  try {
      const photoData = req.body.photo;
      if (!photoData) {
          return res.status(400).send('No photo data.');
      }

      // Convert base64 to buffer
      const buffer = Buffer.from(photoData.split(',')[1], 'base64');
      const filePath = `public/uploads/photo_${Date.now()}.png`;

      // Save the photo to the server
      fs.writeFileSync(filePath, buffer);

      // Process image using OpenAI API
      const result = await PreciseResponse(filePath);

      // Render 'result.ejs' with the result data
      res.render('result', { imageUrl: filePath, result });
  } catch (error) {
      console.error("Error processing photo:", error);
      res.status(500).send('Error processing photo.');
  }
});


// import express from "express";
// import path from "path";
// import multer from "multer";
// import { processImage } from "./openai-test.js"; // Adjust the path as per your project structure
// import { fileURLToPath } from 'url'; // Import fileURLToPath to convert URL to file path
// import router from "./routes.js";


// const app = express();

// app.set("port", process.env.PORT || 3000);

// const __filename = fileURLToPath(import.meta.url);
// const __dirname = path.dirname(__filename);

// app.set("views", path.join(__dirname, "views"));
// app.set("view engine", "ejs"); // Ensure view engine is set to 'ejs'

// // Serve static files from the 'public' directory
// app.use(express.static(path.join(__dirname, 'public')));

// app.use(router);


// // Configure multer for handling file uploads
// const storage = multer.diskStorage({
//   destination: function (req, file, cb) {
//     cb(null, 'uploads/'); // Adjust the directory as per your preference
//   },
//   filename: function (req, file, cb) {
//     cb(null, Date.now() + path.extname(file.originalname)); // Ensure unique filenames
//   }
// });

// const upload = multer({ storage: storage });

// // POST route to handle image uploads
// app.post('/upload', upload.single('image'), async (req, res) => {
//     try {
//       if (!req.file) {
//         return res.status(400).send('No files were uploaded.');
//       }
  
//       const imageUrl = `/uploads/${req.file.filename}`; // Adjust based on your file storage
  
//       // Process image using OpenAI API
//       const result = await processImage(imageUrl);
  
//       res.render('result', { imageUrl, result }); // Render a result page with the output
//     } catch (error) {
//       console.error("Error processing image:", error);
//       res.status(500).send('Error processing image.');
//     }
//   });

// // Define routes
// app.get('/', (req, res) => {
//   res.render('index'); // Render your index.ejs file
// });

// // Start the server
// const PORT = process.env.PORT || 3000;
// app.listen(PORT, () => {
//   console.log(`Server started on port ${PORT}`);
// });