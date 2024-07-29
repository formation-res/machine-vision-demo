from flask import Flask, request, jsonify, send_from_directory
from PIL import Image
from flask_cors import CORS
import numpy as np
from transformers import BlipProcessor, BlipForConditionalGeneration
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import requests


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
colorOptions = [
    'Default', 'LightGrey', 'Grey', 'Black', 'LightGreen', 'LightGreenAlt', 'Green', 'GreenAlt',
    'DarkGreen', 'AquaMarine', 'Turquoise', 'LightBlue', 'LightBlueAlt', 'Blue', 'DarkBlue',
    'Yellow', 'Orange', 'DarkOrange', 'Red', 'DarkRed', 'DarkMagenta', 'White', 'BlueMidnight',
    'BlueSky', 'BlueLavender', 'GraySilver', 'GraySteel', 'GraySlate', 'GreenMoss', 'GreenTurquoise',
    'GreenMint', 'GreenSoft', 'GreenVibrant', 'GreenFresh', 'RedDarkCrimson', 'RedFire', 'RedSalmon',
    'OrangePeach', 'OrangeAmber', 'OrangeRust'
]

textModel = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
iconEmbeddings = textModel.encode(iconOptions)
colorEmbeddings = textModel.encode(colorOptions)

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

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
    
def get_best_color(description, icon):

    descriptionWords = description.split()

    for word in descriptionWords:

        descriptionEmbedding = textModel.encode(word)

        descriptionVector = np.array(descriptionEmbedding).reshape(1, -1)

        similarities = cosine_similarity(descriptionVector, colorEmbeddings)
        similarities.flatten()
        threshold = .5
        mostSimilar = -1
        index = -1
        
        for i in range (0, len(similarities[0])):
            if similarities[0][i] > mostSimilar:
                index = i
                mostSimilar = similarities[0][i]
        if (mostSimilar > threshold):
            print("good color found with", word)
            return colorOptions[index]

    iconEmbedding = textModel.encode(icon)

    iconVector = np.array(iconEmbedding).reshape(1, -1)

    similarities = cosine_similarity(iconVector, colorEmbeddings)
    similarities.flatten()

    mostSimilar = -1
    index = -1
    for i in range (0, len(similarities[0])):
        if similarities[0][i] > mostSimilar:
            index = i
            mostSimilar = similarities[0][i]
    
    return colorOptions[index]

def get_image_description(img_path):
    
    #image = process_image(img_path) can be used to shrink large images

    image = Image.open(img_path)


    #get description of image
    print("getting icon description...")
    inputs = processor(image, "the main focus of this image is ", return_tensors="pt")
    out = model.generate(**inputs)
    description = processor.decode(out[0], skip_special_tokens=True)[32:]
    print("description: ", description)

    return description


def predict(img_path):

    #get image description
    image_description = get_image_description(img_path)

    #get title (right now, just image description)
    title_prediction = image_description

    #get best icon from description
    icon_prediction = get_best_icon(image_description)

    #get color from description
    color_prediction = get_best_color(image_description, icon_prediction)

    update_sophie_pin(image_description, icon_prediction, color_prediction)

    return "title: " + title_prediction + "<br>icon: " + icon_prediction + "<br>color: " + color_prediction



app = Flask(__name__, static_url_path='', static_folder='.')
CORS(app)  # This will enable CORS for all routes

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/classify', methods=['POST'])
def classify():
    #find uploaded file

    print("classifying")

    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file part in the request'}), 400

    file = request.files['file']
    print("predicting")
    #get prediction
    prediction = predict(file)

    #package and return results to javascript
    result = {"message": "Python function called successfully", "data": prediction}

    return jsonify(result)


def update_pete_pin(description, icon, color):

    url = 'https://ahoy-berlin.tryformation.com/objects/legacy/points/IJicTAN8eBClA1d1l8QUgA'

    json_payload = {"latLon":{"lat":52.54129166036981,"lon":13.390654161760267},
                    "connectedToId":"-HN8FcwaRyS7co7XIeIshw",
                    "title": "Pete Pin",
                    "keywords":[],
                    "fieldValueTags":[],
                    "iconCategory": icon,
                    "color": color,
                    "shape":"Circle"}

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJFZERTQSJ9.eyJzdWIiOiJNdmk5OEp6RVdlNVcxVTF0aXkxVG1RIiwid29ya3NwYWNlIjoiYWhveS1iZXJsaW4iLCJzY29wZSI6IkFjY2VzcyIsImlzcyI6InRyeWZvcm1hdGlvbi5jb20iLCJleHAiOjE3MjIzMzE0NjksImlhdCI6MTcyMjI0NTA2OSwid29ya3NwYWNlSWQiOiJJTWp3WW5wM25QU1didGRaRlVwckNBIn0.PZ2KkYauMx9nCX5BSbZ3CG5zP7q97fpk-lzlWotiTXbolF1mmfP5jw-lmF84FgjqVzUTwkAdKsjGlDumSfShDg',
    }

    requests.put(url, json=json_payload, headers=headers)

    url = 'https://ahoy-berlin.tryformation.com/objects/apply-changes'

    json_payload = [{"objectId":"IJicTAN8eBClA1d1l8QUgA","changes":[{"type":"SetDescription","content":description}]}]

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJFZERTQSJ9.eyJzdWIiOiJNdmk5OEp6RVdlNVcxVTF0aXkxVG1RIiwid29ya3NwYWNlIjoiYWhveS1iZXJsaW4iLCJzY29wZSI6IkFjY2VzcyIsImlzcyI6InRyeWZvcm1hdGlvbi5jb20iLCJleHAiOjE3MjIzMzE0NjksImlhdCI6MTcyMjI0NTA2OSwid29ya3NwYWNlSWQiOiJJTWp3WW5wM25QU1didGRaRlVwckNBIn0.PZ2KkYauMx9nCX5BSbZ3CG5zP7q97fpk-lzlWotiTXbolF1mmfP5jw-lmF84FgjqVzUTwkAdKsjGlDumSfShDg',
    }

def update_sophie_pin(description, icon, color):

    url = 'https://ahoy-berlin.tryformation.com/objects/legacy/points/pWUACfAPQ6Z0wOUNj51iig'

    json_payload = {"latLon":{"lat":52.54108999811743,"lon":13.390482454878907},
                    "connectedToId":"-HN8FcwaRyS7co7XIeIshw",
                    "title":"testing door",
                    "keywords":[],
                    "fieldValueTags":[],
                    "iconCategory":icon,
                    "color":color,
                    "shape":"TriangleDown"}

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJFZERTQSJ9.eyJzdWIiOiJNdmk5OEp6RVdlNVcxVTF0aXkxVG1RIiwid29ya3NwYWNlIjoiYWhveS1iZXJsaW4iLCJzY29wZSI6IkFjY2VzcyIsImlzcyI6InRyeWZvcm1hdGlvbi5jb20iLCJleHAiOjE3MjIzMzE0NjksImlhdCI6MTcyMjI0NTA2OSwid29ya3NwYWNlSWQiOiJJTWp3WW5wM25QU1didGRaRlVwckNBIn0.PZ2KkYauMx9nCX5BSbZ3CG5zP7q97fpk-lzlWotiTXbolF1mmfP5jw-lmF84FgjqVzUTwkAdKsjGlDumSfShDg',
    }

    requests.put(url, json=json_payload, headers=headers)

    url = 'https://ahoy-berlin.tryformation.com/objects/apply-changes'

    json_payload = [{"objectId":"pWUACfAPQ6Z0wOUNj51iig","changes":[{"type":"SetDescription","content":description}]}]

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJFZERTQSJ9.eyJzdWIiOiJNdmk5OEp6RVdlNVcxVTF0aXkxVG1RIiwid29ya3NwYWNlIjoiYWhveS1iZXJsaW4iLCJzY29wZSI6IkFjY2VzcyIsImlzcyI6InRyeWZvcm1hdGlvbi5jb20iLCJleHAiOjE3MjIzMzE0NjksImlhdCI6MTcyMjI0NTA2OSwid29ya3NwYWNlSWQiOiJJTWp3WW5wM25QU1didGRaRlVwckNBIn0.PZ2KkYauMx9nCX5BSbZ3CG5zP7q97fpk-lzlWotiTXbolF1mmfP5jw-lmF84FgjqVzUTwkAdKsjGlDumSfShDg',
    }

    requests.post(url, json=json_payload, headers=headers)




if __name__ == '__main__':
    app.run(host='0.0.0.0', ssl_context=('server.crt', 'server.key'), port=5500)
