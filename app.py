import io
from flask import Flask, request, jsonify, send_from_directory
from PIL import Image
from flask_cors import CORS
import requests
import base64
import requests
import json

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

app = Flask(__name__, static_url_path='', static_folder='.')
CORS(app)  # This will enable CORS for all routes
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/classifyWithOpenAI', methods=['POST'])
def classifyWithOpenAI():
    
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    objectId = request.form['objectId']
    workspace = request.form['workspace']
    workspaceId = request.form['workspaceId']

    print("predicting")
    #get prediction
    prediction = predictWithOpenAi(file, objectId, workspace, workspaceId)

    #package and return results to javascript
    result = {"message": "Python function called successfully", "data": prediction}

    return jsonify(result)

def update_pin(description, icon, color, keywords, objectId, workspace, workspaceId):
   
    apiToken = {formationapitoken}
    
    #get original info about the pin
    url = "https://api.tryformation.com/objects/" + objectId
    json_payload = [{"id": objectId}]
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + apiToken,
    }
    original = requests.get(url=url, headers=headers)
    print("code: ", original.status_code)
    originalData = original.json()
    print("data: ", originalData)

    originalLatLon = originalData.get('latLon', {})
    originalConnectedToId = originalData.get('ConnectedTo')
    originalTitle = originalData.get('title')
    originalShape = originalData.get('shape')

    #update the pin with generated info
    url = 'https://' + workspace + '.tryformation.com/objects/legacy/points/' + objectId
    json_payload = {"latLon":originalLatLon,
                    "connectedToId":originalConnectedToId,
                    "title": originalTitle,
                    "keywords":keywords,
                    "fieldValueTags":[],
                    "iconCategory": icon,
                    "color": color,
                    "shape":originalShape}
    requests.put(url, json=json_payload, headers=headers)

    #update description
    url = 'https://ahoy-berlin.tryformation.com/objects/apply-changes'

    json_payload = [{"objectId":objectId,"changes":[{"type":"SetDescription","content":description}]}]
    
    requests.post(url, json=json_payload, headers=headers)
    

def predictWithOpenAi(file_storage, objectId, workspace, workspaceId):

    #convert image to jpeg
    image = Image.open(file_storage)
    converted_image = io.BytesIO()
    image.convert('RGB').save(converted_image, format='JPEG')
    converted_image.seek(0)

    #convert to base64
    image_data = converted_image.read()
    base64_image = base64.b64encode(image_data).decode('utf-8') 

    #get OpenAI response
    api_key = {your API key}

    headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {api_key}"
    }

    prompt = (
        "I need a JSON file with the following strings: Color, Icon, and Description. I also need a list of keywords in the JSON."
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
        "to represent this image, or choose 'Location' if you are not sure. Also, write a short description of the focus of the image as if it was a caption. Lastly, "
        "write 10 important words or phrases describing the image: these should include any extremely relevant text present in the image, including but not limited to "
	" container codes, titles, license plates. All of this, including the color, icon, description, and words/phrases should be included in a JSON file. "
	"only return this JSON file without ``` at the start and finish. The output should have no extraneous grave accent symbols."

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

    print('sending OpenAI request')
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    print('recieved OpenAI response')

    
    # Parse the JSON data
    input_string = response.json()['choices'][0]['message']['content']
    if input_string.startswith('```json') and input_string.endswith('```'):
        input_string = input_string[7:-3].strip()
    print("response: ", input_string) 
    
    data = json.loads(input_string)

    if (data['Color']):
        Color = data['Color']
    else:
        Color = data['color']
    if (data['Icon']):
        Icon = data['Icon']
    else:
        Icon = data['icon']
    if (data['Description']):
        Description = data['Description']
    else:
        Description = data['description']
    if (data['Keywords']):
        Keywords = data['Keywords']
    else:
        Keywords = data['keywords']

    # Checking for made-up icons/colors
    if Icon not in iconOptions:
        print("invalid icon ", Icon, " switching to default.")
        Icon = "Default"
    
    if Color not in colorOptions:
        print("invalid color ", Color, " switching to default.")
        Color = "Default"
    
    #write display for html page
    result_display = "Icon: " + Icon + "<br>Color: " + Color + "<br>Description: " + Description + "<br>Keywords: "
    for word in Keywords:
        result_display = result_display + word + ", "
    result_display = result_display[0:-2]
    
    #update Formation pin 
    update_pin(Description, Icon, Color, Keywords, objectId, workspace, workspaceId)
    
    return result_display


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
