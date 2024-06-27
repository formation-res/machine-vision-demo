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


//-------------------------------------------------------------------------------------------------------------
export async function generateKeywords(imagePath) {
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
            { type: 'text', text: 'Generate keywords to describe the following image.' },

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

export async function chooseIcon(imagePath) {
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
            { type: 'text', text: 'Choose one item from this list that best represents this image and its contents: Location, Flag, Megaphone, Block, Bolt, Cluster, Coffee, Information, PaintBrush, Tools, Turkey, Apple, Badge, Boxes, Setting, Cupcake, Toilet, Shop, FireExtinguisher, NoAccess, Security, Equipment, Lightbulb, Gear, Electricity, Desk, Printer, Forklift, Helmet, Car, Train, Bin, Folder, Computer, AGV, Robot, Projector, Toolbox, API, Bicycle, Door, Elevator, Exit, FaceMask, FirstAid, Food, GolfCart, Defibrillator, Medical, MeetingRoom, NoPhone, NoSmoking, OfficeDesk, Parking, QRCode, SecurityCamera, Server, Star, UserGroup, WiFi, WirelessDoorLock, Caution, ArrowRight, Camera, WaterFaucet, Stairs, Event, Task, Building, User, Object, AGVBosch, Booth, FoodTruck, FormationLogo, GeoCaching, Milkrun, Prize, Regal, SingelBox, Stage, NFC, TrackedObject, Container, Coil, Tablet, CameraDrone, Clip, Flashlight, Notebook, Scissors, VRGlasses, Clipboard, Whiteboard, Pen, Flooding, ClearanceVehicle, Antenna, RoadBlock, Fire, Rubble, SixFeetApart, AirPortShuttle, Ambulance, Apartment, BabyChangingStation, Bed, PhoneChargingStation, Ferry, Family, GenderFemale, GenderMale, GenderDiverse, Hospital, NightShelter, Church, Embassy, FireFighter, InformationAlt, MoneyExchange, PoliceOfficer, DangerExplosions, DangerAerialBombs, DangerAerialBombsAlt, Tank, Departures, BioHazard, Bricks, PassageForbidden, HighVoltage, Ladder, LocationAlt, PowerPlug, OldTelephone, MeetingPoint, MeetingPointAlt, Pets, Translate, TelephoneTypeWriter, WheelChairPickup, RatTrap, Barrier, BarrierAlt, MetroStation, Vaccination, Passport, Pin, AidBadge, AidTag, PaperTowels, Chemicals, Crane, HeartRate, DisplayGraph, Mortar, Mattress, TaskMedic, FolderMedic, Syringe, BandAids, BloodPressure, Cardiogram, EyeDropper, HospitalBed, HospitalBedAlt, Lifter, ScaleAnalog, Pills, PillsBottle, PillsBox, HandTruck, ScaleDigital, ShoppingCart, Stethoscope, Thermostat, UpDown, Dingo, Eagle, Multi, Patriot, Wolf, Axle, WaitAT, WaitET, Gears, Engine, Zone, Tag, Cake, BirthdayCake, Cheese, Beer, Pint, Wineglass, Box, Microphone, Sausage, Music, SmileyGood, SmileyAlright, SmileyNotGood, SmileyHappy, SmileyAfraid.  If no icon represents it well, choose "default". Respond with the exact icon you choose and nothing else.' },
            
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

export async function PreciseResponse(imagePath) {
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
            { type: 'text', text: 'Here is a list of colors: LightGrey, Grey, Black, LightGreen, LightGreenAlt, Green, GreenAlt, DarkGreen, AquaMarine, Turquoise, LightBlue, LightBlueAlt, Blue, DarkBlue, Yellow, Orange, DarkOrange, Red, DarkRed, DarkMagenta, White, BlueMidnight, BlueSky, BlueLavender, GraySilver, GraySteel, GraySlate, GreenMoss, GreenTurquoise, GreenMint, GreenSoft, GreenVibrant, GreenFresh, RedDarkCrimson, RedFire, RedSalmon, OrangePeach, OrangeAmber, OrangeRust. Choose one color from this list of colors to represent this image, or say "LightGrey" if you are not sure. Here is a list of icons: Location, Flag, Megaphone, Block, Bolt, Cluster, Coffee, Information, PaintBrush, Tools, Turkey, Apple, Badge, Boxes, Setting, Cupcake, Toilet, Shop, FireExtinguisher, NoAccess, Security, Equipment, Lightbulb, Gear, Electricity, Desk, Printer, Forklift, Helmet, Car, Train, Bin, Folder, Computer, AGV, Robot, Projector, Toolbox, API, Bicycle, Door, Elevator, Exit, FaceMask, FirstAid, Food, GolfCart, Defibrillator, Medical, MeetingRoom, NoPhone, NoSmoking, OfficeDesk, Parking, QRCode, SecurityCamera, Server, Star, UserGroup, WiFi, WirelessDoorLock, Caution, ArrowRight, Camera, WaterFaucet, Stairs, Event, Task, Building, User, Object, AGVBosch, Booth, FoodTruck, FormationLogo, GeoCaching, Milkrun, Prize, Regal, SingelBox, Stage, NFC, TrackedObject, Container, Coil, Tablet, CameraDrone, Clip, Flashlight, Notebook, Scissors, VRGlasses, Clipboard, Whiteboard, Pen, Flooding, ClearanceVehicle, Antenna, RoadBlock, Fire, Rubble, SixFeetApart, AirPortShuttle, Ambulance, Apartment, BabyChangingStation, Bed, PhoneChargingStation, Ferry, Family, GenderFemale, GenderMale, GenderDiverse, Hospital, NightShelter, Church, Embassy, FireFighter, InformationAlt, MoneyExchange, PoliceOfficer, DangerExplosions, DangerAerialBombs, DangerAerialBombsAlt, Tank, Departures, BioHazard, Bricks, PassageForbidden, HighVoltage, Ladder, LocationAlt, PowerPlug, OldTelephone, MeetingPoint, MeetingPointAlt, Pets, Translate, TelephoneTypeWriter, WheelChairPickup, RatTrap, Barrier, BarrierAlt, MetroStation, Vaccination, Passport, Pin, AidBadge, AidTag, PaperTowels, Chemicals, Crane, HeartRate, DisplayGraph, Mortar, Mattress, TaskMedic, FolderMedic, Syringe, BandAids, BloodPressure, Cardiogram, EyeDropper, HospitalBed, HospitalBedAlt, Lifter, ScaleAnalog, Pills, PillsBottle, PillsBox, HandTruck, ScaleDigital, ShoppingCart, Stethoscope, Thermostat, UpDown, Dingo, Eagle, Multi, Patriot, Wolf, Axle, WaitAT, WaitET, Gears, Engine, Zone, Tag, Cake, BirthdayCake, Cheese, Beer, Pint, Wineglass, Box, Microphone, Sausage, Music, SmileyGood, SmileyAlright, SmileyNotGood, SmileyHappy, SmileyAfraid. Choose one icon from this list of icons to represent this image, or choose "Location" if you are not sure. Lastly, come up with exactly 10 keywords that describe this image. Respond exactly like this: "Icon: ", the icon chosen from the given list, "Color: ", the color chosen from the given list, "Keywords: ", the 10 keywords. Everything should be separated by a comma, and there should be no new lines (\n) in the response.' },
            
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

    //get data from model's response
    const array = parseResponse(response.choices[0].message.content);
    console.log(array);


    return response.choices[0].message.content;
  } catch (error) {
    console.error('Error processing image:', error);
    throw error; // Handle errors appropriately in your application
  }
}

function parseResponse(inputString) {
  // Split the input string by ', ' to get individual components
  const parts = inputString.split(', ');
  // Extract color and icon from the first two parts
  let icon = parts[0].replace('Icon: ', ''); // Extract color
  let color = parts[1].replace('Color: ', '');   // Extract icon
  const keyword1 = parts[2].replace('Keywords: ', '');

  const icons = [
    "Default", "Location", "Flag", "Megaphone", "Block", "Bolt", "Cluster", "Coffee", "Information", 
    "PaintBrush", "Tools", "Turkey", "Apple", "Badge", "Boxes", "Setting", "Cupcake", "Toilet", 
    "Shop", "FireExtinguisher", "NoAccess", "Security", "Equipment", "Lightbulb", "Gear", 
    "Electricity", "Desk", "Printer", "Forklift", "Helmet", "Car", "Train", "Bin", "Folder", 
    "Computer", "AGV", "Robot", "Projector", "Toolbox", "API", "Bicycle", "Door", "Elevator", 
    "Exit", "FaceMask", "FirstAid", "Food", "GolfCart", "Defibrillator", "Medical", "MeetingRoom", 
    "NoPhone", "NoSmoking", "OfficeDesk", "Parking", "QRCode", "SecurityCamera", "Server", "Star", 
    "UserGroup", "WiFi", "WirelessDoorLock", "Caution", "ArrowRight", "Camera", "WaterFaucet", 
    "Stairs", "Event", "Task", "Building", "User", "Object", "AGVBosch", "Booth", "FoodTruck", 
    "FormationLogo", "GeoCaching", "Milkrun", "Prize", "Regal", "SingelBox", "Stage", "NFC", 
    "TrackedObject", "Container", "Coil", "Tablet", "CameraDrone", "Clip", "Flashlight", "Notebook", 
    "Scissors", "VRGlasses", "Clipboard", "Whiteboard", "Pen", "Flooding", "ClearanceVehicle", 
    "Antenna", "RoadBlock", "Fire", "Rubble", "SixFeetApart", "AirPortShuttle", "Ambulance", 
    "Apartment", "BabyChangingStation", "Bed", "PhoneChargingStation", "Ferry", "Family", 
    "GenderFemale", "GenderMale", "GenderDiverse", "Hospital", "NightShelter", "Church", "Embassy", 
    "FireFighter", "InformationAlt", "MoneyExchange", "PoliceOfficer", "DangerExplosions", 
    "DangerAerialBombs", "DangerAerialBombsAlt", "Tank", "Departures", "BioHazard", "Bricks", 
    "PassageForbidden", "HighVoltage", "Ladder", "LocationAlt", "PowerPlug", "OldTelephone", 
    "MeetingPoint", "MeetingPointAlt", "Pets", "Translate", "TelephoneTypeWriter", "WheelChairPickup", 
    "RatTrap", "Barrier", "BarrierAlt", "MetroStation", "Vaccination", "Passport", "Pin", "AidBadge", 
    "AidTag", "PaperTowels", "Chemicals", "Crane", "HeartRate", "DisplayGraph", "Mortar", "Mattress", 
    "TaskMedic", "FolderMedic", "Syringe", "BandAids", "BloodPressure", "Cardiogram", "EyeDropper", 
    "HospitalBed", "HospitalBedAlt", "Lifter", "ScaleAnalog", "Pills", "PillsBottle", "PillsBox", 
    "HandTruck", "ScaleDigital", "ShoppingCart", "Stethoscope", "Thermostat", "UpDown", "Dingo", 
    "Eagle", "Multi", "Patriot", "Wolf", "Axle", "WaitAT", "WaitET", "Gears", "Engine", "Zone", 
    "Tag", "Cake", "BirthdayCake", "Cheese", "Beer", "Pint", "Wineglass", "Box", "Microphone", 
    "Sausage", "Music", "SmileyGood", "SmileyAlright", "SmileyNotGood", "SmileyHappy", "SmileyAfraid", 
    "SmileyDead", "SmileyLaugh", "SmileyOk", "SmileySmile", "SmileySad", "SmileyOuch", "SmileyQuiet", 
    "SmileyUpsideDown", "Heatmap", "WheelChair", "Wardrobe", "Handbag", "Hanger", "WrenchSet", 
    "Screwdrivers", "LadderAlt", "JackStand", "HandScanner", "Hammer", "GreaseGun", "Drill", 
    "DiagnosticTool", "AirCompressor", "Drain", "FluidDrop", "WaterSupply", "WaterBottle", "WaterGlass", 
    "Drinks", "Cocktail", "WineBottle"
  ];
  const colors = [
    "Default", "LightGrey", "Grey", "Black", "LightGreen", "LightGreenAlt", "Green", "GreenAlt", 
    "DarkGreen", "AquaMarine", "Turquoise", "LightBlue", "LightBlueAlt", "Blue", "DarkBlue", 
    "Yellow", "Orange", "DarkOrange", "Red", "DarkRed", "DarkMagenta", "White", "BlueMidnight", 
    "BlueSky", "BlueLavender", "GraySilver", "GraySteel", "GraySlate", "GreenMoss", "GreenTurquoise", 
    "GreenMint", "GreenSoft", "GreenVibrant", "GreenFresh", "RedDarkCrimson", "RedFire", 
    "RedSalmon", "OrangePeach", "OrangeAmber", "OrangeRust"
  ];

  //checking for made up icons/colors
  if(!icons.includes(icon)) {
    console.log("invalid icon, switching to default.");
    icon = "Default";
  }
  if(!colors.includes(color)) {
    console.log("invalid color, switching to default.");
    color = "Default";
  }

  // Extract keywords from the remaining parts
  const keywords = parts.slice(3);

  // Construct the result array
  const result = [icon, color, keyword1, ...keywords];

  return result;
}
