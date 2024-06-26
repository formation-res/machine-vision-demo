import OpenAI from "openai";
import fs from 'fs';
import path from 'path';

const openai = new OpenAI();

// export async function processImage(imageUrl) {
//     try {
//         const response = await openai.chat.completions.create({
//           model: "gpt-4o",
//           messages: [
//             {
//               role: "user",
//               content: [
//                 { type: "text", text: "What’s in this image?" },
//                 {
//                   type: "image_url",
//                   image_url: {
//                     url: imageUrl,
//                   },
//                 },
//               ],
//             },
//           ],
//         });
//         return response.choices[0].message.content; // Adjust as per API response structure
//     } catch (error) {
//       console.error("Error processing image:", error);
//       throw error; // Handle errors appropriately in your application
//     }
// }


export async function processImage(imagePath) {
  try {
    // Function to encode the image as base64
    function encodeImage(imagePath) {
      const imageData = fs.readFileSync(imagePath);
      return Buffer.from(imageData).toString('base64');
    }

    // Get the base64-encoded image data
    const base64Image = encodeImage(imagePath);

    // Construct payload for OpenAI API request
    const payload = {
      model: 'gpt-4o',
      messages: [
        {
          role: 'user',
          content: [
            { type: 'text', text: 'What’s in this image?' },
            {
              type: 'image_url',
              image_url: {
                url: `data:image/jpeg;base64,${base64Image}`,
              },
            },
          ],
        },
      ],
      max_tokens: 300,
    };

    // Make API request to OpenAI
    const response = await openai.chat.completions.create(payload);
    return response.choices[0].message.content;
  } catch (error) {
    console.error('Error processing image:', error);
    throw error; // Handle errors appropriately in your application
  }
}
