const message = document.querySelector("#message")
const message2 = document.querySelector("#message2")
const fileButton = document.querySelector("#file")
const img = document.querySelector("#img")
const synth = window.speechSynthesis
  
//all icon options, their text embeddings, and the text model.
let iconOptions = ['Location', 'Flag', 'Megaphone', 'Block', 'Bolt', 'Cluster', 'Coffee', 'Information', 'PaintBrush', 'Tools', 'Turkey', 'Apple', 'Badge', 'Boxes', 'Setting', 'Cupcake', 'Toilet', 'Shop', 'FireExtinguisher', 'NoAccess', 'Security', 'Equipment', 'Lightbulb', 'Gear', 'Electricity', 'Desk', 'Printer', 'Forklift', 'Helmet', 'Car', 'Train', 'Bin', 'Folder', 'Computer', 'AGV', 'Robot', 'Projector', 'Toolbox', 'API', 'Bicycle', 'Door', 'Elevator', 'Exit', 'FaceMask', 'FirstAid', 'Food', 'GolfCart', 'Defibrillator', 'Medical', 'MeetingRoom', 'NoPhone', 'NoSmoking', 'OfficeDesk', 'Parking', 'QRCode', 'SecurityCamera', 'Server', 'Star', 'UserGroup', 'WiFi', 'WirelessDoorLock', 'Caution', 'ArrowRight', 'Camera', 'WaterFaucet', 'Stairs', 'Event', 'Task', 'Building', 'User', 'Object', 'AGVBosch', 'Booth', 'FoodTruck', 'FormationLogo', 'GeoCaching', 'Milkrun', 'Prize', 'Regal', 'SingelBox', 'Stage', 'NFC', 'TrackedObject', 'Container', 'Coil', 'Tablet', 'CameraDrone', 'Clip', 'Flashlight', 'Notebook', 'Scissors', 'VRGlasses', 'Clipboard', 'Whiteboard', 'Pen', 'Flooding', 'ClearanceVehicle', 'Antenna', 'RoadBlock', 'Fire', 'Rubble', 'SixFeetApart', 'AirPortShuttle', 'Ambulance', 'Apartment', 'BabyChangingStation', 'Bed', 'PhoneChargingStation', 'Ferry', 'Family', 'GenderFemale', 'GenderMale', 'GenderDiverse', 'Hospital', 'NightShelter', 'Church', 'Embassy', 'FireFighter', 'InformationAlt', 'MoneyExchange', 'PoliceOfficer', 'DangerExplosions', 'DangerAerialBombs', 'DangerAerialBombsAlt', 'Tank', 'Departures', 'BioHazard', 'Bricks', 'PassageForbidden', 'HighVoltage', 'Ladder', 'LocationAlt', 'PowerPlug', 'OldTelephone', 'MeetingPoint', 'MeetingPointAlt', 'Pets', 'Translate', 'TelephoneTypeWriter', 'WheelChairPickup', 'RatTrap', 'Barrier', 'BarrierAlt', 'MetroStation', 'Vaccination', 'Passport', 'Pin', 'AidBadge', 'AidTag', 'PaperTowels', 'Chemicals', 'Crane', 'HeartRate', 'DisplayGraph', 'Mortar', 'Mattress', 'TaskMedic', 'FolderMedic', 'Syringe', 'BandAids', 'BloodPressure', 'Cardiogram', 'EyeDropper', 'HospitalBed', 'HospitalBedAlt', 'Lifter', 'ScaleAnalog', 'Pills', 'PillsBottle', 'PillsBox', 'HandTruck', 'ScaleDigital', 'ShoppingCart', 'Stethoscope', 'Thermostat', 'UpDown', 'Dingo', 'Eagle', 'Multi', 'Patriot', 'Wolf', 'Axle', 'WaitAT', 'WaitET', 'Gears', 'Engine', 'Zone', 'Tag', 'Cake', 'BirthdayCake', 'Cheese', 'Beer', 'Pint', 'Wineglass', 'Box', 'Microphone', 'Sausage', 'Music', 'SmileyGood', 'SmileyAlright', 'SmileyNotGood', 'SmileyHappy', 'SmileyAfraid'];
let iconEmbeddings = [];
let textModel;

SetupTextModel(); //set up iconEmbeddings and textModel

//let classifier;
const classifier = ml5.imageClassifier('MobileNet', {version: 2}, modelLoaded);


//load file when a file is added
fileButton.addEventListener("change", event => loadFile(event))
img.addEventListener("load", () => userImageUploaded())


function loadFile(event) {
  img.src = URL.createObjectURL(event.target.files[0]);
}

//PYTHON CLASSIFICATION METHOD
//uses a model run through python and the word semantics model to recommend an icon
async function classifyWithPython() {

  //get file data
  const fileInput = document.getElementById('fileInput');
  const file = fileInput.files[0];
  const formData = new FormData();
  formData.append('file', file);

  //Call Python function via Flask API
  try {
    const response = await fetch('http://127.0.0.1:5500/classify', {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    //collect results
    const result = await response.json();
    console.log(result.data);

    //match python predictions to icons
    pythonResult = await findMostSimilarPair([result.data])

    //display results
    message2.innerHTML = `Python icon: ${pythonResult.option} <br />based on: ${pythonResult.result}`;

  } catch (err) {
    console.error('Error calling Python function:', err);
  }
  
}

//---------------------ML5 CLASSIFICATION STUFF-------------------------

async function userImageUploaded() {
  message.innerHTML = "Image was loaded!";
  message2.innerHTML = "";

  try {
    const predictions = await classifier.classify(img);
    handleClassification(predictions);
  } catch (err) {
    console.error(err);
  }
}

async function handleClassification(predictions) {

  // Adjust confidence based on stringList
  predictions.forEach(result => {
    stringList.forEach(string => {
      if (result.label.toLowerCase() === string.toLowerCase()) {
        result.confidence *= 1.5; // Increase confidence by 50%
      }
    });
  });

  // Sort with highest confidence first
  predictions.sort((a, b) => b.confidence - a.confidence);

  // Pass results to text model and display final results
  displayResults(predictions);
}


async function displayResults(results) {
  
  //pass confident image classifications to text model
  let modelRecommendationString = "";
  for (let i = 0; i < results.length; i++) {
    if (results[i].confidence > .5 || i == 0) { //confidence threshold
      modelRecommendationString += results[i].label;
      modelRecommendationString += ' ';
    }
  }
  //find best icon based on image classifications
  finalResult = await findMostSimilarPair([modelRecommendationString]);
  
  //display results on page and in console
  message.innerHTML = `I think it's a ${results[0].label} with confidence ${results[0].confidence.toFixed(2)}!<br />
  Best icon: ${finalResult.option} <br />based on: ${finalResult.result}`;
  
  //console.log("final results:", await finalResult);

  results.forEach(result => {
    //console.log(`${result.label}: ${result.confidence.toFixed(2)}`);
  });
}

//-------------------------------------TEXT MODEL STUFF-------------------------------------------------

async function SetupTextModel() {
  try {
    // Ensure TensorFlow.js is ready and set the backend
    await tf.ready();
    
    // Load the model
    textModel = await use.load();

    //get icon embeddings
    for (i in iconOptions) {
      let tempIconEmbedding = await textModel.embed(iconOptions[i]);
      iconEmbeddings.push(await tempIconEmbedding.array());
    }

    //tell user text model is ready
    textModelLoaded();

  } catch (error) {
    console.error("Error running the model:", error);
  }
}

function cosineSimilarity(vec1, vec2) {
  // Calculate dot product
  let dotProduct = 0;
  for (let i = 0; i < vec1.length; i++) {
      dotProduct += vec1[i] * vec2[i];
  }

  // Calculate norms
  let norm1 = 0;
  let norm2 = 0;
  for (let i = 0; i < vec1.length; i++) {
      norm1 += vec1[i] * vec1[i];
      norm2 += vec2[i] * vec2[i];
  }
  norm1 = Math.sqrt(norm1);
  norm2 = Math.sqrt(norm2);

  // Calculate cosine similarity
  const similarity = dotProduct / (norm1 * norm2);
  return similarity;
}

// Function to find the most similar pair.
async function findMostSimilarPair(modelRecommendations) {
  let maxSimilarity = -1;
  let mostSimilarPair = { result: '', option: '' };

  //console.log("Model recommends:", modelRecommendations);

  const modelRecommendationsEbedding = [];

  for (i in modelRecommendations) {
    let tempEmbedding = await textModel.embed(modelRecommendations[i]);
    modelRecommendationsEbedding.push(await tempEmbedding.array());
  }

  for (i = 0; i < await modelRecommendations.length; i++) {
    for (j = 0; j < iconOptions.length; j++) {

      // Calculate cosine similarity between embeddings.
      const similarity = cosineSimilarity(modelRecommendationsEbedding[i][0], iconEmbeddings[j][0]);


      // Update max similarity and most similar pair if current pair is more similar.
      if (similarity > maxSimilarity) {
        maxSimilarity = similarity;
        mostSimilarPair = { result: modelRecommendations[i], option: iconOptions[j] };
      }
    }
  }

  return mostSimilarPair;
}


//Tells user when models are ready to be used

function modelLoaded() {
  console.log('Image Classification Model Loaded!');
  message.innerHTML = "Image Classification Model loaded!"
}

function textModelLoaded() {
  console.log('Text Model Loaded!');
  message2.innerHTML = "Text model loaded!"
}





//adding strings to the site, representing previous pins
//doesn't really do anything rn, previous implementation was useless

let stringList = []; // Array to store the entered strings
//let stringList = ['Location', 'Flag', 'Megaphone', 'Block', 'Bolt', 'Cluster', 'Coffee', 'Information', 'PaintBrush', 'Tools', 'Turkey', 'Apple', 'Badge', 'Boxes', 'Setting', 'Cupcake', 'Toilet', 'Shop', 'FireExtinguisher', 'NoAccess', 'Security', 'Equipment', 'Lightbulb', 'Gear', 'Electricity', 'Desk', 'Printer', 'Forklift', 'Helmet', 'Car', 'Train', 'Bin', 'Folder', 'Computer', 'AGV', 'Robot', 'Projector', 'Toolbox', 'API', 'Bicycle', 'Door', 'Elevator', 'Exit', 'FaceMask', 'FirstAid', 'Food', 'GolfCart', 'Defibrillator', 'Medical', 'MeetingRoom', 'NoPhone', 'NoSmoking', 'OfficeDesk', 'Parking', 'QRCode', 'SecurityCamera', 'Server', 'Star', 'UserGroup', 'WiFi', 'WirelessDoorLock', 'Caution', 'ArrowRight', 'Camera', 'WaterFaucet', 'Stairs', 'Event', 'Task', 'Building', 'User', 'Object', 'AGVBosch', 'Booth', 'FoodTruck', 'FormationLogo', 'GeoCaching', 'Milkrun', 'Prize', 'Regal', 'SingelBox', 'Stage', 'NFC', 'TrackedObject', 'Container', 'Coil', 'Tablet', 'CameraDrone', 'Clip', 'Flashlight', 'Notebook', 'Scissors', 'VRGlasses', 'Clipboard', 'Whiteboard', 'Pen', 'Flooding', 'ClearanceVehicle', 'Antenna', 'RoadBlock', 'Fire', 'Rubble', 'SixFeetApart', 'AirPortShuttle', 'Ambulance', 'Apartment', 'BabyChangingStation', 'Bed', 'PhoneChargingStation', 'Ferry', 'Family', 'GenderFemale', 'GenderMale', 'GenderDiverse', 'Hospital', 'NightShelter', 'Church', 'Embassy', 'FireFighter', 'InformationAlt', 'MoneyExchange', 'PoliceOfficer', 'DangerExplosions', 'DangerAerialBombs', 'DangerAerialBombsAlt', 'Tank', 'Departures', 'BioHazard', 'Bricks', 'PassageForbidden', 'HighVoltage', 'Ladder', 'LocationAlt', 'PowerPlug', 'OldTelephone', 'MeetingPoint', 'MeetingPointAlt', 'Pets', 'Translate', 'TelephoneTypeWriter', 'WheelChairPickup', 'RatTrap', 'Barrier', 'BarrierAlt', 'MetroStation', 'Vaccination', 'Passport', 'Pin', 'AidBadge', 'AidTag', 'PaperTowels', 'Chemicals', 'Crane', 'HeartRate', 'DisplayGraph', 'Mortar', 'Mattress', 'TaskMedic', 'FolderMedic', 'Syringe', 'BandAids', 'BloodPressure', 'Cardiogram', 'EyeDropper', 'HospitalBed', 'HospitalBedAlt', 'Lifter', 'ScaleAnalog', 'Pills', 'PillsBottle', 'PillsBox', 'HandTruck', 'ScaleDigital', 'ShoppingCart', 'Stethoscope', 'Thermostat', 'UpDown', 'Dingo', 'Eagle', 'Multi', 'Patriot', 'Wolf', 'Axle', 'WaitAT', 'WaitET', 'Gears', 'Engine', 'Zone', 'Tag', 'Cake', 'BirthdayCake', 'Cheese', 'Beer', 'Pint', 'Wineglass', 'Box', 'Microphone', 'Sausage', 'Music', 'SmileyGood', 'SmileyAlright', 'SmileyNotGood', 'SmileyHappy', 'SmileyAfraid']

function addString() {
    let inputElement = document.getElementById('stringInput');
    let inputValue = inputElement.value.trim(); // Trim any leading/trailing whitespace
    
    if (inputValue !== '') {
      stringList.push(inputValue); // Add the string to the array
        inputElement.value = ''; // Clear the input field
        displayStrings(); // Update the displayed strings
    }
}

function displayStrings() {
    let listElement = document.getElementById('stringList');
    listElement.innerHTML = ''; // Clear previous content

    stringList.forEach(function(string) {
        let listItem = document.createElement('li');
        listItem.textContent = string;
        listElement.appendChild(listItem);
    });
}
