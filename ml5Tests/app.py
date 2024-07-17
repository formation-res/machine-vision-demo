from flask import Flask, request, jsonify
from PIL import Image
from flask_cors import CORS
import numpy as np
import os
from transformers import BlipProcessor, BlipForConditionalGeneration
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer


iconOptions = [
  'Location', 'Flag', 'Megaphone', 'Block', 'Bolt', 'Cluster', 'Coffee', 'Information',
  'PaintBrush', 'Tools', 'Turkey', 'Apple', 'Badge', 'Boxes', 'Setting', 'Cupcake', 
  'Toilet', 'Shop', 'FireExtinguisher', 'NoAccess', 'Security', 'Equipment', 'Lightbulb',
  'Gear', 'Electricity', 'Desk', 'Printer', 'Forklift', 'Helmet', 'Car', 'Train', 'Bin',
  'Folder', 'Computer', 'AGV', 'Robot', 'Projector', 'Toolbox', 'API', 'Bicycle', 'Door',
  'Elevator', 'Exit', 'FaceMask', 'FirstAid', 'Food', 'GolfCart', 'Defibrillator', 'Medical',
  'MeetingRoom', 'NoPhone', 'NoSmoking', 'OfficeDesk', 'Parking', 'QRCode', 'SecurityCamera',
  'Server', 'Star', 'UserGroup', 'WiFi', 'WirelessDoorLock', 'Caution', 'ArrowRight', 'Camera',
  'WaterFaucet', 'Stairs', 'Event', 'Task', 'Building', 'User', 'Object', 'AGVBosch', 'Booth',
  'FoodTruck', 'FormationLogo', 'GeoCaching', 'Milkrun', 'Prize', 'Regal', 'SingelBox', 'Stage',
  'NFC', 'TrackedObject', 'Container', 'Coil', 'Tablet', 'CameraDrone', 'Clip', 'Flashlight',
  'Notebook', 'Scissors', 'VRGlasses', 'Clipboard', 'Whiteboard', 'Pen', 'Flooding',
  'ClearanceVehicle', 'Antenna', 'RoadBlock', 'Fire', 'Rubble', 'SixFeetApart', 'AirPortShuttle',
  'Ambulance', 'Apartment', 'BabyChangingStation', 'Bed', 'PhoneChargingStation', 'Ferry', 'Family',
  'GenderFemale', 'GenderMale', 'GenderDiverse', 'Hospital', 'NightShelter', 'Church', 'Embassy',
  'FireFighter', 'InformationAlt', 'MoneyExchange', 'PoliceOfficer', 'DangerExplosions',
  'DangerAerialBombs', 'DangerAerialBombsAlt', 'Tank', 'Departures', 'BioHazard', 'Bricks',
  'PassageForbidden', 'HighVoltage', 'Ladder', 'LocationAlt', 'PowerPlug', 'OldTelephone',
  'MeetingPoint', 'MeetingPointAlt', 'Pets', 'Translate', 'TelephoneTypeWriter', 'WheelChairPickup',
  'RatTrap', 'Barrier', 'BarrierAlt', 'MetroStation', 'Vaccination', 'Passport', 'Pin', 'AidBadge',
  'AidTag', 'PaperTowels', 'Chemicals', 'Crane', 'HeartRate', 'DisplayGraph', 'Mortar', 'Mattress',
  'TaskMedic', 'FolderMedic', 'Syringe', 'BandAids', 'BloodPressure', 'Cardiogram', 'EyeDropper',
  'HospitalBed', 'HospitalBedAlt', 'Lifter', 'ScaleAnalog', 'Pills', 'PillsBottle', 'PillsBox',
  'HandTruck', 'ScaleDigital', 'ShoppingCart', 'Stethoscope', 'Thermostat', 'UpDown', 'Dingo',
  'Eagle', 'Multi', 'Patriot', 'Wolf', 'Axle', 'WaitAT', 'WaitET', 'Gears', 'Engine', 'Zone',
  'Tag', 'Cake', 'BirthdayCake', 'Cheese', 'Beer', 'Pint', 'Wineglass', 'Box', 'Microphone',
  'Sausage', 'Music', 'SmileyGood', 'SmileyAlright', 'SmileyNotGood', 'SmileyHappy', 'SmileyAfraid',
  'SmileyDead', 'SmileyLaugh', 'SmileyOk', 'SmileySmile', 'SmileySad', 'SmileyOuch', 'SmileyQuiet',
  'SmileyUpsideDown', 'Heatmap', 'WheelChair', 'Wardrobe', 'Handbag', 'Hanger', 'WrenchSet',
  'Screwdrivers', 'LadderAlt', 'JackStand', 'HandScanner', 'Hammer', 'GreaseGun', 'Drill',
  'DiagnosticTool', 'AirCompressor', 'Drain', 'FluidDrop', 'WaterSupply', 'WaterBottle',
  'WaterGlass', 'Drinks', 'Cocktail', 'WineBottle'
]

textModel = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
iconEmbeddings = textModel.encode(iconOptions)

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")


def get_best_icon(description):

    descriptionEmbedding = textModel.encode(description)

    descriptionVector = np.array(descriptionEmbedding).reshape(1, -1)

    similarities = cosine_similarity(descriptionVector, iconEmbeddings)
    similarities.flatten()

    mostSimilar = -1
    index = -1
    for i in range (0, len(similarities[0])):
        if similarities[0][i] > mostSimilar:
            index = i
            mostSimilar = similarities[0][i]
    return iconOptions[index]

def process_image(img_path):

    raw_image = Image.open(img_path)
    max_dimension = 256
    width, height = raw_image.size
    
    # Calculate the aspect ratio of the image
    aspect_ratio = width / float(height)
    
    # Calculate dimensions for resizing
    if width > height:
        new_width = max_dimension
        new_height = int(max_dimension / aspect_ratio)
    else:
        new_height = max_dimension
        new_width = int(max_dimension * aspect_ratio)
    
    # Resize the image
    resized_image = raw_image.resize((new_width, new_height))
    return resized_image
    


def predict(img_path):

    image = process_image(img_path)

    #get description of image
    print("getting icon description...")
    inputs = processor(image, "the main focus of this image is ", return_tensors="pt")
    out = model.generate(**inputs)
    output = processor.decode(out[0], skip_special_tokens=True)[32:]
    print("description: ", output)

    #get best icon from description
    icon_prediction = get_best_icon(output)

    return icon_prediction



app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route('/classify', methods=['POST'])
def classify():
    #find uploaded file
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file part in the request'}), 400

    file = request.files['file']
    filepath = "uploads\\" + file.filename

    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'}), 400

    #temporarily save file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    #get prediction
    prediction = predict(filepath)

    #delete file
    try:
        os.remove(file_path)
    except Exception as e:
        print(f"Error deleting file: {e}")
        return jsonify({'success': False, 'error': 'Error deleting file'}), 500

    #package and return results to javascript
    result = {"message": "Python function called successfully", "data": prediction}

    return jsonify(result)




if __name__ == '__main__':
    app.run(debug=True, port=5500)


