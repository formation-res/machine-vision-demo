import io
from flask import Flask, request, jsonify, send_from_directory
from PIL import Image
from flask_cors import CORS
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
    
    #get original info about the pin
    url = "https://api.tryformation.com/objects/" + objectId
    json_payload = [{"id": objectId}]
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {apitoken}',
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

    #update description (currently always gives a blank description)
    url = 'https://ahoy-berlin.tryformation.com/objects/apply-changes'

    json_payload = [{"objectId":objectId,"changes":[{"type":"SetDescription","content":description}]}]
    
    requests.post(url, json=json_payload, headers=headers)
    

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
        'Authorization': 'Bearer {apitoken}'
    }

    requests.put(url, json=json_payload, headers=headers)

    url = 'https://ahoy-berlin.tryformation.com/objects/apply-changes'

    json_payload = [{"objectId":"IJicTAN8eBClA1d1l8QUgA","changes":[{"type":"SetDescription","content":description}]}]

    requests.post(url, json=json_payload, headers=headers)


def update_sophie_pin(description, icon, color, keywords):

    url = 'https://ahoy-berlin.tryformation.com/objects/legacy/points/pWUACfAPQ6Z0wOUNj51iig'

    json_payload = {"latLon":{"lat":52.541101005969497,"lon":13.390478414663676},
                    "connectedToId":"-HN8FcwaRyS7co7XIeIshw",
                    "title":"testing door",
                    "keywords":keywords,
                    "fieldValueTags":[],
                    "iconCategory":icon,
                    "color":color,
                    "shape":"Heart"}

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {apitoken}',
    }

    requests.put(url, json=json_payload, headers=headers)

    url = 'https://ahoy-berlin.tryformation.com/objects/apply-changes'

    json_payload = [{"objectId":"pWUACfAPQ6Z0wOUNj51iig","changes":[{"type":"SetDescription","content":description}]}]

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {apitoken}',
    }

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
    api_key = {your api key}

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
        "to represent this image, or choose 'Location' if you are not sure. If there is any major and relevant text in the image, including and limited to license plates, labels, and codes,"
        "please respond only the most important text (from the given options). For example, the text should be in a format similar to this: '1ABC234'. If there is too much relevant text (over 5 words), do not provide any text."
        "If none of the text is much more important than the rest of the image, do not provide any text. This text should generally be no more than 2 words long. Lastly, come up with exactly 10 keywords that describe this image. "
        "If there is no relevant text or too many details, do not include the text in the response. If there is relevant text, include it after the icon and color. Respond exactly like this: 'Icon: ', the icon "
        "chosen from the given list, 'Color: ', the color chosen from the given list, if there is any relevant text, it should go here. then the 10 keywords should follow immediately. Everything should be separated by a "
        "comma, and there should be no new lines (\\n) in the response."
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

    print('hihi1')
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    print('hihi')

    print(response)

    #response string to be cut
    input_string = response.json()['choices'][0]['message']['content']
    print("response: ", input_string)
    #separate response
    parts = input_string.split(', ')
    
    icon = parts[0].replace('Icon: ', '')
    color = parts[1].replace('Color: ', '')
    keyword1 = parts[2].replace('Keywords: ', '')

    # Checking for made-up icons/colors
    if icon not in iconOptions:
        print("invalid icon ", icon, " switching to default.")
        icon = "Default"
    
    if color not in colorOptions:
        print("invalid color ", color, " switching to default.")
        color = "Default"

    # Extract keywords from the remaining parts
    keywords = parts[3:]
    result = [icon, color, keyword1] + keywords

    #update pin
    update_pin("", icon, color, [keyword1] + keywords, objectId, workspace, workspaceId)
    #update_sophie_pin("", icon, color, [keyword1] + keywords)
    print(icon, color)
    
    result_display = "Icon selected: " + icon + "<br>Color selected: " + color + "<br>Keywords selected: " + keyword1
    for word in keywords:
        result_display = result_display + ", " + word

    

    return result_display


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
