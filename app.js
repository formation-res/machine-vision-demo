// Import necessary modules
import express from "express";
import path from "path";
import multer from "multer";
import { processImage } from "./openai-test.js";
import { fileURLToPath } from 'url';
// import router from "./routes.js";

const app = express();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

app.set("port", process.env.PORT || 3000);
app.set("views", path.join(__dirname, "views"));
app.set("view engine", "ejs");

// Serve static files (e.g., CSS, images) from the 'public' directory
app.use(express.static(path.join(__dirname, 'public')));

// app.use(router);

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
    const result = await processImage(imageUrl);

    // Render 'result.ejs' with the result data
    res.render('result', { imageUrl, result });
  } catch (error) {
    console.error("Error processing image:", error);
    res.status(500).send('Error processing image.');
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server started on port ${PORT}`);
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

