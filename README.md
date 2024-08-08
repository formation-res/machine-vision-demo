# FORMATION Pin Data Generator Demo

## Overview

This project is a demo developed by Sophie Zhu and Pete Sullivan for FORMATION. It showcases a powerful tool designed to enhance the digital map within the FORMATION app or website by generating comprehensive data for a location or object (called a pin) using computer vision.

## Features

- **Computer Vision Integration:** Utilizes OpenAI's GPT-4 vision model to generate detailed data for any pin from an image uploaded by the user.
- **Real-Time Updates:** The generated data, including descriptions, visual icons, colors, keywords, and more, is added to FORMATION's database via API calls, updating the pin on the app/website in real time.
- **Efficient Processing:** Although a local, pretrained computer vision model combined with text-to-vector embedding is functional, it is not used due to the superior speed of the GPT-4 vision model.

## How It Works

1. **Image Upload:** Users upload an image of a location or object (pin) within the FORMATION app or website.
2. **Data Generation:** The image is processed using OpenAI's GPT-4 vision model to generate descriptive data, visual icons, colors, and keywords.
3. **Database Update:** The generated data is sent to FORMATION's database through API calls, updating the pin in real time on the digital map.

## Usage

This demo is run within FORMATION's servers and is designed to seamlessly integrate with the existing infrastructure of the FORMATION app and website. 

## Installation and Setup

Since this demo runs within FORMATION's servers, installation and setup instructions are not provided here. For any development or deployment queries, please contact the project maintainers.

## Video Demonstration

https://github.com/user-attachments/assets/ca8413fd-d785-4b18-bf00-f4e8a40483a6

## Contributors

- **Sophie Zhu**
- **Pete Sullivan**

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For any questions or support, please contact:

- Sophie Zhu: sophie.zhuyy@gmail.com
- Pete Sullivan: petesullivanis@gmail.com

---

Thank you for using the FORMATION Pin Data Generator Demo. We hope it enhances your experience with the FORMATION app and website!
