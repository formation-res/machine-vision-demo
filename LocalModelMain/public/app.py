import io
from flask import Flask, request, jsonify, send_from_directory
from PIL import Image
from flask_cors import CORS
import numpy as np
from transformers import BlipProcessor, BlipForConditionalGeneration
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import requests
import base64
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

    #update_pete_pin(image_description, icon_prediction, color_prediction, [])

    return "title: " + title_prediction + "<br>icon: " + icon_prediction + "<br>color: " + color_prediction



app = Flask(__name__, static_url_path='', static_folder='.')
CORS(app)  # This will enable CORS for all routes

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/classify', methods=['POST'])
def classify():

    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file part in the request'}), 400

    file = request.files['file']
    print("predicting")
    #get prediction
    prediction = predict(file)

    #package and return results to javascript
    result = {"message": "Python function called successfully", "data": prediction}

    return jsonify(result)

@app.route('/classifyWithOpenAI', methods=['POST'])
def classifyWithOpenAI():

    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file part in the request'}), 400

    file = request.files['file']
    print("predicting")
    #get prediction
    prediction = predictWithOpenAi(file)

    #package and return results to javascript
    result = {"message": "Python function called successfully", "data": prediction}

    return jsonify(result)


def update_pete_pin(description, icon, color, keywords):

    url = 'https://ahoy-berlin.tryformation.com/objects/legacy/points/IJicTAN8eBClA1d1l8QUgA'

    json_payload = {"latLon":{"lat":52.54129166036981,"lon":13.390654161760267},
                    "connectedToId":"-HN8FcwaRyS7co7XIeIshw",
                    "title": "Pete Pin",
                    "keywords":keywords,
                    "fieldValueTags":[],
                    "iconCategory": icon,
                    "color": color,
                    "shape":"Circle"}

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJFZERTQSJ9.eyJzdWIiOiJuemRKZVlKVjVMeWVMQXJFR1hyN1FBIiwid29ya3NwYWNlIjoiYWhveS1iZXJsaW4iLCJzY29wZSI6IkFjY2VzcyIsImlzcyI6InRyeWZvcm1hdGlvbi5jb20iLCJleHAiOjE3MjIzMzE0ODQsImlhdCI6MTcyMjI0NTA4NCwid29ya3NwYWNlSWQiOiJJTWp3WW5wM25QU1didGRaRlVwckNBIn0.URrpJRKQ5YIrELiBpE4uRCme3xJOnKHALJvWlAk3h_u_hEYI4qwH_QhtTrG5JjL_rb49eZvbCvWjvUMWUKxACA',
    }

    requests.put(url, json=json_payload, headers=headers)

    url = 'https://ahoy-berlin.tryformation.com/objects/apply-changes'

    json_payload = [{"objectId":"IJicTAN8eBClA1d1l8QUgA","changes":[{"type":"SetDescription","content":description}]}]

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJFZERTQSJ9.eyJzdWIiOiJuemRKZVlKVjVMeWVMQXJFR1hyN1FBIiwid29ya3NwYWNlIjoiYWhveS1iZXJsaW4iLCJzY29wZSI6IkFjY2VzcyIsImlzcyI6InRyeWZvcm1hdGlvbi5jb20iLCJleHAiOjE3MjIzMzE0ODQsImlhdCI6MTcyMjI0NTA4NCwid29ya3NwYWNlSWQiOiJJTWp3WW5wM25QU1didGRaRlVwckNBIn0.URrpJRKQ5YIrELiBpE4uRCme3xJOnKHALJvWlAk3h_u_hEYI4qwH_QhtTrG5JjL_rb49eZvbCvWjvUMWUKxACA',
    }

    requests.post(url, json=json_payload, headers=headers)



def predictWithOpenAi(file_storage):

    #convert image to jpeg
    image = Image.open(file_storage)
    converted_image = io.BytesIO()
    image.convert('RGB').save(converted_image, format='JPEG')
    converted_image.seek(0)

    #convert to base64
    image_data = converted_image.read()
    base64_image = base64.b64encode(image_data).decode('utf-8') 

    #get OpenAI response
    api_key = "api-key"

    headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {api_key}"
    }

    prompt = (
        "Here is a list of colors: LightGrey, Grey, Black, LightGreen, LightGreenAlt, Green, GreenAlt, "
        "DarkGreen, AquaMarine, Turquoise, LightBlue, LightBlueAlt, Blue, DarkBlue, Yellow, Orange, DarkOrange, "
        "Red, DarkRed, DarkMagenta, White, BlueMidnight, BlueSky, BlueLavender, GraySilver, GraySteel, GraySlate, "
        "GreenMoss, GreenTurquoise, GreenMint, GreenSoft, GreenVibrant, GreenFresh, RedDarkCrimson, RedFire, "
        "RedSalmon, OrangePeach, OrangeAmber, OrangeRust. Choose one color from this list of colors to represent this image, "
        "or say 'LightGrey' if you are not sure. Here is a list of icons: Location, Flag, Megaphone, Block, Bolt, Cluster, "
        "Coffee, Information, PaintBrush, Tools, Turkey, Apple, Badge, Boxes, Setting, Cupcake, Toilet, Shop, FireExtinguisher, "
        "NoAccess, Security, Equipment, Lightbulb, Gear, Electricity, Desk, Printer, Forklift, Helmet, Car, Train, Bin, Folder, "
        "Computer, AGV, Robot, Projector, Toolbox, API, Bicycle, Door, Elevator, Exit, FaceMask, FirstAid, Food, GolfCart, "
        "Defibrillator, Medical, MeetingRoom, NoPhone, NoSmoking, OfficeDesk, Parking, QRCode, SecurityCamera, Server, Star, "
        "UserGroup, WiFi, WirelessDoorLock, Caution, ArrowRight, Camera, WaterFaucet, Stairs, Event, Task, Building, User, Object, "
        "AGVBosch, Booth, FoodTruck, FormationLogo, GeoCaching, Milkrun, Prize, Regal, SingelBox, Stage, NFC, TrackedObject, Container, "
        "Coil, Tablet, CameraDrone, Clip, Flashlight, Notebook, Scissors, VRGlasses, Clipboard, Whiteboard, Pen, Flooding, ClearanceVehicle, "
        "Antenna, RoadBlock, Fire, Rubble, SixFeetApart, AirPortShuttle, Ambulance, Apartment, BabyChangingStation, Bed, PhoneChargingStation, "
        "Ferry, Family, GenderFemale, GenderMale, GenderDiverse, Hospital, NightShelter, Church, Embassy, FireFighter, InformationAlt, MoneyExchange, "
        "PoliceOfficer, DangerExplosions, DangerAerialBombs, DangerAerialBombsAlt, Tank, Departures, BioHazard, Bricks, PassageForbidden, HighVoltage, "
        "Ladder, LocationAlt, PowerPlug, OldTelephone, MeetingPoint, MeetingPointAlt, Pets, Translate, TelephoneTypeWriter, WheelChairPickup, RatTrap, Barrier, "
        "BarrierAlt, MetroStation, Vaccination, Passport, Pin, AidBadge, AidTag, PaperTowels, Chemicals, Crane, HeartRate, DisplayGraph, Mortar, Mattress, TaskMedic, "
        "FolderMedic, Syringe, BandAids, BloodPressure, Cardiogram, EyeDropper, HospitalBed, HospitalBedAlt, Lifter, ScaleAnalog, Pills, PillsBottle, PillsBox, HandTruck, "
        "ScaleDigital, ShoppingCart, Stethoscope, Thermostat, UpDown, Dingo, Eagle, Multi, Patriot, Wolf, Axle, WaitAT, WaitET, Gears, Engine, Zone, Tag, Cake, BirthdayCake, "
        "Cheese, Beer, Pint, Wineglass, Box, Microphone, Sausage, Music, SmileyGood, SmileyAlright, SmileyNotGood, SmileyHappy, SmileyAfraid. Choose one icon from this list of icons "
        "to represent this image, or choose 'Location' if you are not sure. Lastly, come up with exactly 10 keywords that describe this image. Respond exactly like this: 'Icon: ', the icon "
        "chosen from the given list, 'Color: ', the color chosen from the given list, 'Keywords: ', the 10 keywords. Everything should be separated by a comma, and there should be no new lines (\\n) in the response."
    )

    payload = {
      "model": "gpt-4o",
      "messages": [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": prompt
            },
            {
              "type": "image_url",
              "image_url": {
                "url": f'data:image/jpeg;base64,{base64_image}'
              }
            }
          ]
        }
      ],
      "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    #response string to be cut
    input_string = response.json()['choices'][0]['message']['content']

    #separate response
    parts = input_string.split(', ')
    
    icon = parts[0].replace('Icon: ', '')
    color = parts[1].replace('Color: ', '')
    keyword1 = parts[2].replace('Keywords: ', '')

    # Checking for made-up icons/colors
    if icon not in iconOptions:
        print("invalid icon, switching to default.")
        icon = "Default"
    
    if color not in colorOptions:
        print("invalid color, switching to default.")
        color = "Default"

    # Extract keywords from the remaining parts
    keywords = parts[3:]
    result = [icon, color, keyword1] + keywords

    #update pin
    update_pete_pin("", icon, color, [keyword1] + keywords)

    return result


if __name__ == '__main__':
    app.run(host='0.0.0.0', ssl_context=('server.crt', 'server.key'), port=5500)