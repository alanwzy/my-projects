# Import libraries
from flask import Flask
from flask import request
import requests
import json
import mysql.connector
import random
from dateutil import parser
import pandas as pd
import datetime
import itertools
import operator
from flask_cors import CORS


# ------------------------------------------------------------------------------
# ----------------------- Define the auxiliary functions -----------------------
# ------------------------------------------------------------------------------

# STATIC variables
OPENUV_URL_RECENT = "https://api.openuv.io/api/v1/uv"
OPENUV_URL_FORECAST = "https://api.openuv.io/api/v1/forecast"
ACCUWEATHER_URL_GEO_SEARCH = "http://dataservice.accuweather.com/locations/v1/cities/geoposition/search"
ACCUWEATHER_URL_FORECAST = "http://dataservice.accuweather.com/forecasts/v1/daily/5day/{key}"
ACCUWEATHER_URL_INDICES = "http://dataservice.accuweather.com/indices/v1/daily/5day/{key}/groups/11"


# This function reads the text file contains the OpenUV API keys and randomly return 1 of them
def get_api_key():
    all_keys = []
    f = open('open_uv_api_keys.txt', 'r')
    lines = f.readlines()
    for l in lines:
        all_keys.append(str(l).rstrip())
    return random.choice(all_keys)

# This function reads the text file contains the AccuWeather API keys and randomly return 1 of them
def get_api_key_i3():
    all_keys = []
    f = open('accu_weather_api_keys.txt', 'r')
    lines = f.readlines()
    for l in lines:
        all_keys.append(str(l).rstrip())
    return random.choice(all_keys)


# This function return a connection to the database
def connect_to_db():
    # Get azure authentication
    all_info = []
    f = open('azure_database_authentication.txt', 'r')
    lines = f.readlines()
    for l in lines:
        all_info.append(str(l).rstrip())
        
    db_info = {
        'server_name': all_info[0],
        'user_name': all_info[1],
        'pwd': all_info[2],
        'db_name': all_info[3] 
    }

    return mysql.connector.connect(
        host=db_info['server_name'],
        user=db_info['user_name'],
        password=db_info['pwd'],
        database=db_info['db_name']
    )


# This function find the given suburb info from the database
def find_coordinate(postcode):
    db_connection = connect_to_db()
    db_cursor = db_connection.cursor()
    
    # If valid post code then return actual result
    try:
        db_cursor.execute("SELECT * FROM suburbs WHERE postcode="+postcode)
        record = db_cursor.fetchall()[0]
        coord = {
            'lat': record[4],
            'lng': record[3]
        }
        suburb_info = {
            'postcode': record[1],
            'name': record[2]
        }
    # If invalid post code then return default result
    except Exception:
        coord = {
            'lat': '-37.817403',
            'lng': '144.956776'
        }
        suburb_info = {
            'postcode': '3000',
            'name': 'Default postcode: 3000'
        }
    # Always return data instead of error
    finally:
        return [coord, suburb_info]


# Define the function to evaluate the UVR
def evaluate_uvr(uvr):
    if uvr<=2:
        return 'low'
    elif uvr>2 and uvr<=5:
        return 'relative low'
    elif uvr>5 and uvr<=7:
        return 'moderate'
    elif uvr>7 and uvr<=10:
        return 'high'
    else:
        return 'extremely high'

# Get the content for activity by its ID
def get_activity_name(id):
    if id == 1:
        return "running"
    elif id == 2:
        return "jogging"
    elif id == 3:
        return "hiking"
    elif id == 4:
        return "bicycling"
    elif id == 5:
        return "golf"
    elif id == 6:
        return "tennis"
    elif id == 7:
        return "skateboarding"
    elif id == 8:
        return "outdoor_concert"
    elif id == 9:
        return "kite_flying"
    elif id == 10:
        return "swimming"
    elif id == 11:
        return "sailing"
    elif id == 13:
        return "fishing"
    elif id == 15:
        return "skiing"
    elif id == 24:
        return "bbq"
    else:
        return "lawn_mowing"


# Function to rcheck recommended activities, type=0: excellent_activities, type=1: poor_activities
def check_activites(list_of_activities):
    if len(list_of_activities)==0:
        return ["Stay Home"]
    else:
        return list_of_activities

# Function to convert datetime to string
def convert_date(date_type):
    str_type = str(date_type)
    return str(parser.parse(str_type).date())

# Function to convert UTC to AUS time
def convert_to_AUS(utc_date):
    aus_time = parser.parse(utc_date) + datetime.timedelta(hours=10)
    aus_time = str(aus_time.time().hour) + ":" + str(aus_time.time().minute)
    return aus_time

# Function to evaluate UVR to get Low and Medium periods of the day
def evaluate_uvr_i3(uvr):
    if uvr < 3:
        return "L"
    elif (uvr >= 3 and uvr < 6):
        return "M"
    else:
        return "H"


# Function to round-up time
def round_minute(hour_minute, forward=True):
    hour = int(str(hour_minute).split(":")[0])
    minute = int(str(hour_minute).split(":")[1])
    
    # Round time up
    if forward:
        if minute<=15:
            return str(hour) + ":15"
        elif minute>15 and minute<=30:
            return str(hour) + ":30"
        elif minute>30 and minute<=45:
            return str(hour) + ":45"
        else:
            return str(hour+1) + ":00"
    # Round time down
    else:
        if minute<=15:
            return str(hour) + ":00"
        elif minute>15 and minute<=30:
            return str(hour) + ":15"
        elif minute>30 and minute<=45:
            return str(hour) + ":30"
        else:
            return str(hour) + ":45"



# -----------------------------------------------------------------------
# ------------------------ Create the Aplication ------------------------
# -----------------------------------------------------------------------
app = Flask(__name__)
CORS(app)


# -------------------------------------------------------------------------------
# ------------------------------ Generate the APIs ------------------------------
# -------------------------------------------------------------------------------


# ------------------------------------- ITERATION 1 -------------------------------------

# API to get current UVR for a specific location (Iteration 1)
@app.route('/uvr_location')
def uvr_location():

    postcode = request.args.get('postcode')
    
    # Get coordinates from database
    PARAMS = find_coordinate(postcode)[0]
    suburb_info = find_coordinate(postcode)[1]

    # Get the data
    try:
        # Send API request to OpenUV
        req = requests.get(url=OPENUV_URL_RECENT, params=PARAMS, headers={"x-access-token": get_api_key()})
        data = json.loads(req.text)
        
        # Compose and return result data
        result = {
            'postcode': postcode,
            'suburb': suburb_info['name'],
            'UVR': data['result']['uv'],
            'max_UVR': data['result']['uv_max']
        }
    # Return default data if error occurs
    except Exception:
        # Compose and return result data
        result = {
            'postcode': postcode,
            'suburb': suburb_info['name'],
            'UVR': 0,
            'max_UVR': 6
        }
    # Always return data instead of error
    finally:
        return str(result)
    



# API to get current UVR for 18 most crowded suburbs in Melbourne (Iteration 1)
@app.route('/uvr_inner_suburbs')
def uvr_inner_suburbs():
    # 18 most crowded suburbs in Melbourne
    INNER_SUBURBS = ['3000', '3121', '3182', '3056', '3141', '3051', 
                    '3181', '3053', '3006', '3183', '3207', '3184', 
                    '3068', '3057', '3031', '3065', '3162', '3168']
    # Get the data
    try:
        # List of data to return
        result = list()

        # Get data for each postcode
        for postcode in INNER_SUBURBS:
            # Get coordinates from database
            PARAMS = find_coordinate(postcode)[0]
            suburb_info = find_coordinate(postcode)[1]
            
            # Send API request to OpenUV
            req = requests.get(url=OPENUV_URL_RECENT, params=PARAMS, headers={"x-access-token": get_api_key()})
            data = json.loads(req.text)
            
            # Compose result data
            result.append({
                'postcode': postcode,
                'suburb': suburb_info['name'],
                'UVR': data['result']['uv'],
                'max_UVR': data['result']['uv_max']
            })
    # Return defalut data if error occurs
    except Exception:
        result = [
            { 'postcode': '3000', 'suburb': 'MELBOURNE', 'UVR': 0, 'max_UVR': 6 }, 
            { 'postcode': '3121', 'suburb': 'BURNLEY', 'UVR': 0, 'max_UVR': 6 }, 
            { 'postcode': '3182', 'suburb': 'ST KILDA', 'UVR': 0, 'max_UVR': 6 }, 
            { 'postcode': '3056', 'suburb': 'BRUNSWICK', 'UVR': 0, 'max_UVR': 6 }, 
            { 'postcode': '3141', 'suburb': 'CHAPEL STREET NORTH', 'UVR': 0, 'max_UVR': 6 }, 
            { 'postcode': '3051', 'suburb': 'HOTHAM HILL', 'UVR': 0, 'max_UVR': 6 }, 
            { 'postcode': '3181', 'suburb': 'PRAHRAN', 'UVR': 0, 'max_UVR': 6 }, 
            { 'postcode': '3053', 'suburb': 'CARLTON', 'UVR': 0, 'max_UVR': 6 }, 
            { 'postcode': '3006', 'suburb': 'SOUTH WHARF', 'UVR': 0, 'max_UVR': 6 }, 
            { 'postcode': '3183', 'suburb': 'BALACLAVA', 'UVR': 0, 'max_UVR': 6 }, 
            { 'postcode': '3207', 'suburb': 'GARDEN CITY', 'UVR': 0, 'max_UVR': 6 }, 
            { 'postcode': '3184', 'suburb': 'BRIGHTON ROAD', 'UVR': 0, 'max_UVR': 6 }, 
            { 'postcode': '3068', 'suburb': 'CLIFTON HILL', 'UVR': 0, 'max_UVR': 6 }, 
            { 'postcode': '3057', 'suburb': 'BRUNSWICK EAST', 'UVR': 0, 'max_UVR': 6 }, 
            { 'postcode': '3031', 'suburb': 'FLEMINGTON', 'UVR': 0, 'max_UVR': 6 }, 
            { 'postcode': '3065', 'suburb': 'FITZROY', 'UVR': 0, 'max_UVR': 6 }, 
            { 'postcode': '3162', 'suburb': 'CAULFIELD', 'UVR': 0, 'max_UVR': 6 }, 
            { 'postcode': '3168', 'suburb': 'CLAYTON', 'UVR': 0, 'max_UVR': 6 }
        ]
    # Always return data instead of error
    finally:
        return str(result)


# API to get historical UVR group by Months (Iteration 1)
@app.route('/uvr_by_month')
def uv_by_month():
    # Create connection to database
    db_connection = connect_to_db()

    # Create and execute SQL query
    db_cursor = db_connection.cursor()
    db_cursor.execute("SELECT * FROM uvr")
    records = db_cursor.fetchall()

    # List of data to return
    result = []

    # Compose and return result data
    for rec in records:
        result.append({
            'month': rec[1],
            'year': rec[2],
            'avg_UVR': rec[3]
        })
    return str(result)


# API to get historical UVR group by Years (Iteration 1)
@app.route('/uvr_by_year')
def uvr_by_year():
    # Create connection to database
    db_connection = connect_to_db()

    # Create and execute SQL query
    db_cursor = db_connection.cursor()
    db_cursor.execute("SELECT year, AVG(uv_index) AS avg_uv FROM uvr GROUP BY year")
    records = db_cursor.fetchall()

    # List of data to return
    result = []

    # Compose and return result data
    for rec in records:
        result.append({
            'year': rec[0],
            'avg_UVR': rec[1]
        })
    return str(result)


# API to get protectors based on UVR (Iteration 1)
@app.route('/uvr_protector')
def uvr_protector():

    uvr = float(request.args.get('uvr'))
    uvr_rating = evaluate_uvr(uvr)

    result = []
    
    # Query data from DB
    db_connection = connect_to_db()

    # Create and execute SQL query
    db_cursor = db_connection.cursor()

    # Find the hats
    db_cursor.execute("SELECT * FROM hat WHERE UVR='"+uvr_rating+"'")
    records = db_cursor.fetchall()
    
    # Compose result data
    for rec in records:
        result.append({
            'type': 'hat',
            'hat_type': rec[2],
            'forehead': rec[3],
            'cheek': rec[4],
            'nose': rec[5],
            'ear': rec[6],
            'chin': rec[7],
            'neck': rec[8],
        })
    
    # Find the sunglasses
    db_cursor.execute("SELECT * FROM sunglasses WHERE UVR='"+uvr_rating+"'")
    records = db_cursor.fetchall()
    
    # Compose result data
    for rec in records:
        result.append({
            'type': 'sunglasses',
            'lens_category': rec[2],
            'function': rec[3],
            'situation': rec[4],
            'glare': rec[5]
        })

    # Find the sunscreen
    db_cursor.execute("SELECT * FROM sunscreen WHERE UVR='"+uvr_rating+"'")
    records = db_cursor.fetchall()
    
    # Compose result data
    for rec in records:
        if rec[2] == '1':
            pa_str = 'PA+'
        elif rec[2] == '2':
            pa_str = 'PA++'
        elif rec[2] == '3':
            pa_str = 'PA+++'
        elif rec[2] == '4':
            pa_str = 'PA++++'
        else:
            pa_str = 'PA+'

        result.append({
            'type': 'sunscreen',
            'PA': pa_str,
            'desc': rec[3],
            'SPF': rec[4],
            'UVB_percentage': rec[5],
            'situation': rec[6]
        })

    # Find the clohtes
    db_cursor.execute("SELECT * FROM umbrella_clothes WHERE UVB='"+uvr_rating+"'")
    records = db_cursor.fetchall()
    
    # Compose result data
    for rec in records:
        result.append({
            'type': 'umbrella_clothes',
            'UPF': rec[2],
            'UVB_percentage': rec[3]
        })

    return str(result)


# API to return 1 single protector (Iteration 1)
@app.route('/single_protector')
def single_protector():

    protector_name = request.args.get('protector_name')

    # Query data from DB
    db_connection = connect_to_db()

    # Create and execute SQL query
    db_cursor = db_connection.cursor()

    result = []

    # Get all hats
    if protector_name == 'hat':
        db_cursor.execute("SELECT * FROM "+protector_name)
        records = db_cursor.fetchall()
        
        # Compose result data
        for rec in records:
            result.append({
                'hat_type': rec[2],
                'forehead': rec[3],
                'cheek': rec[4],
                'nose': rec[5],
                'ear': rec[6],
                'chin': rec[7],
                'neck': rec[8],
            })
    # Get all sunglasses
    elif protector_name == 'sunglasses':
        db_cursor.execute("SELECT * FROM "+protector_name)
        records = db_cursor.fetchall()
        
        # Compose result data
        for rec in records:
            result.append({
                'lens_category': rec[2],
                'function': rec[3],
                'situation': rec[4],
                'glare': rec[5]
            })
    # Get all sunscreen
    elif protector_name == 'sunscreen':
        db_cursor.execute("SELECT * FROM "+protector_name)
        records = db_cursor.fetchall()
        
        # Compose result data
        for rec in records:
            result.append({
                'PA': rec[2],
                'desc': rec[3],
                'SPF': rec[4],
                'UVB_percentage': rec[5],
                'situation': rec[6]
            })
    # Get all umbrella_clothes
    elif protector_name == 'umbrella_clothes':
        db_cursor.execute("SELECT * FROM "+protector_name)
        records = db_cursor.fetchall()
        
        # Compose result data
        for rec in records:
            result.append({
                'UPF': rec[2],
                'UVB_percentage': rec[3]
            })
    else:   
        return "Invalid Request"

    return str(result)


#  API to return all protectors (Iteration 1)
@app.route('/all_protectors')
def all_protectors():

    result = {}

    # Query data from DB
    db_connection = connect_to_db()

    # Create and execute SQL query
    db_cursor = db_connection.cursor()


    # Get all sunglasses
    temp = []
    db_cursor.execute("SELECT * FROM sunglasses")
    records = db_cursor.fetchall()
    
    # Compose temp data
    for rec in records:
        temp.append({
            'lens_category': rec[2],
            'function': rec[3],
            'situation': rec[4],
            'glare': rec[5]
        })
    # Compose result data
    result['sunglasses'] = temp


    # Get all hat
    temp = []
    db_cursor.execute("SELECT * FROM hat")
    records = db_cursor.fetchall()
    
    # Compose temp data
    for rec in records:
        temp.append({
            'hat_type': rec[2],
            'forehead': rec[3],
            'cheek': rec[4],
            'nose': rec[5],
            'ear': rec[6],
            'chin': rec[7],
            'neck': rec[8],
        })
    # Compose result data
    result['hat'] = temp


    # Get all sunscreen
    temp = []
    db_cursor.execute("SELECT * FROM sunscreen")
    records = db_cursor.fetchall()
    
    # Compose temp data
    for rec in records:
        temp.append({
            'PA': rec[2],
            'desc': rec[3],
            'SPF': rec[4],
            'UVB_percentage': rec[5],
            'situation': rec[6]
        })
    # Compose result data
    result['sunscreen'] = temp


    # Get all umbrella_clothes
    temp = []
    db_cursor.execute("SELECT * FROM umbrella_clothes")
    records = db_cursor.fetchall()
    
    # Compose temp data
    for rec in records:
        temp.append({
            'UPF': rec[2],
            'UVB_percentage': rec[3]
        })
    # Compose result data
    result['umbrella_clothes'] = temp
    
    return str(result)



# ------------------------------------- ITERATION 2 -------------------------------------

# API to get current UVR for a specific location (Iteration 2)
@app.route('/uvr_location_i2')
def uvr_location_i2():

    postcode = request.args.get('postcode')
    
    # Get coordinates from database
    PARAMS = find_coordinate(postcode)[0]
    suburb_info = find_coordinate(postcode)[1]

    # Send API request to OpenUV
    req = requests.get(url=OPENUV_URL_RECENT, params=PARAMS, headers={"x-access-token": get_api_key()})
    data = json.loads(req.text)
    
    # Compose and return result data
    result = {
        'postcode': postcode,
        'suburb': suburb_info['name'],
        'UVR': data['result']['uv'],
        'max_UVR': data['result']['uv_max'],
        'lat': PARAMS['lat'],
        'lng': PARAMS['lng']
    }
    return str(result)


# API to get historical UVR group by Months (Iteration 2)
@app.route('/uv_by_month_i2')
def uv_by_month_i2():
    # Create connection to database
    db_connection = connect_to_db()

    # Create and execute SQL query
    db_cursor = db_connection.cursor()
    db_cursor.execute("SELECT month, AVG(uv_index) AS avg_uv FROM uvr GROUP BY month ORDER BY month ASC")
    records = db_cursor.fetchall()

    # List of data to return
    result = []

    # Compose and return result data
    for rec in records:
        result.append(rec[1])
    
    # Data is a list of Average UVR from [Jan, Feb, Mar,..., Dec]
    return str(result)


# API to get historical UVR group by Years (Iteration 2)
@app.route('/uv_by_year_i2')
def uv_by_year_i2():
    # Create connection to database
    db_connection = connect_to_db()

    # Create and execute SQL query
    db_cursor = db_connection.cursor()
    db_cursor.execute("SELECT year, AVG(uv_index) AS avg_uv FROM uvr GROUP BY year ORDER BY year ASC")
    records = db_cursor.fetchall()

    # List of data to return
    result = []

    # Compose and return result data
    for rec in records:
        result.append(rec[1])

    # Data is a list of Average UVR from [2010, 2011, 2012,..., 2020]
    return str(result)


# API to get hospitals by postcode (Iteration 2)
@app.route('/nearby_hospitals_i2')
def nearby_hospitals_i2():

    postcode = request.args.get('postcode')
    result = []
    
    # Query data from DB
    db_connection = connect_to_db()

    # Create and execute SQL query
    db_cursor = db_connection.cursor()

    # If the postcode is valid then return hospitals nearby
    try:
        # Find the hospitals
        db_cursor.execute("SELECT * FROM hospitals WHERE Postcode="+postcode)
        records = db_cursor.fetchall()
        
        # Compose result data
        for rec in records:
            result.append({
                'name': rec[1],
                'phone': rec[2],
                'address': rec[3],
                'suburb': rec[4],
                'postcode': rec[5],
                'state': rec[6],
                'sector': rec[7],
                'lat': rec[8],
                'lng': rec[9]
            })
    # If the postcode is invalid then return default hospital
    except Exception:
        result.append({
                'name': "Default hospital for invalid postcode: Royal Melbourne Hospital [Parkville]",
                'phone': "03 9342 7000",
                'address': '300 Grattan Street',
                'suburb': 'Parkville',
                'postcode': 3050,
                'state': 'Vic',
                'sector': 'Public',
                'lat': -37.799259,
                'lng': 144.956864
            })
    # Always return data instead of error
    finally:
        if len(result)==0:
            result.append({
                'name': "Default hospital for invalid postcode: Royal Melbourne Hospital [Parkville]",
                'phone': "03 9342 7000",
                'address': '300 Grattan Street',
                'suburb': 'Parkville',
                'postcode': 3050,
                'state': 'Vic',
                'sector': 'Public',
                'lat': -37.799259,
                'lng': 144.956864
            })

        return str(result)

    
# API to get quizzes (Iteration 2)
@app.route('/quiz_i2')
def quiz_i2():
    all_topics = ['Eye_dmg', 'Skin_dmg', 'Sunscreen', 'Sunglasses', 'Hat', 'Cloth', 'UVR']
    
    result = []

    # Query data from DB
    db_connection = connect_to_db()

    # Create and execute SQL query
    db_cursor = db_connection.cursor()

    # Get 1 random question for each topic
    for topic in all_topics:
        db_cursor.execute("SELECT * FROM quiz WHERE Topic='{}' ORDER BY RAND() LIMIT 1".format(topic))
        records = db_cursor.fetchall()

        # Compose the result
        for rec in records:
            result.append({
                'topic': rec[1],
                'question': rec[2],
                'answer': rec[3],
                'explanation': rec[4],
                'selection_1': rec[5],
                'selection_2': rec[6]
            })

    # Return the result
    return str(result)


# ------------------------------------- ITERATION 3 -------------------------------------
# API to get next 5 days (Iteration 3)
@app.route('/next_5days_i3')
def next_5days_i3():
    # Get postcode from URL and get its info from db
    postcode = request.args.get('postcode')
    coord = find_coordinate(postcode)[0]
    suburb_name = find_coordinate(postcode)[1]["name"]
    lat = coord['lat']
    lng = coord['lng']

    # Get the data
    try:
        # Request parameters 1
        PARAMS_1 = {
            "apikey": get_api_key_i3(),
            "q": str(lat) + "," + str(lng),
            "details": "true"
        }
        # Send API request to AccuWeather to convert lat and lng to location key
        req_1 = requests.get(url=ACCUWEATHER_URL_GEO_SEARCH, params=PARAMS_1)
        location_key = json.loads(req_1.text)["Key"]
        
        # Request parameters 2
        PARAMS_2 = {
            "apikey": get_api_key_i3(),
            "details": "true",
            "metric": "true"        
        }
        # Send API request to AccuWeather to get 5days forecast
        req_2 = requests.get(url=ACCUWEATHER_URL_FORECAST.format(key=location_key), params=PARAMS_2)
        data_2 = json.loads(req_2.text)
        new_data_2 = list()
        for day in data_2["DailyForecasts"]:
            new_data_2.append({
                "date": convert_date(day["Date"]),
                "max_uvr": day["AirAndPollen"][-1]["Value"]
            })

        # Request parameters 3
        PARAMS_3 = {
            "apikey": get_api_key_i3(),
            "details": "true"  
        }
        # Send API request to AccuWeather to get activities
        req_3 = requests.get(url=ACCUWEATHER_URL_INDICES.format(key=location_key), params=PARAMS_3)
        data_3 = json.loads(req_3.text)
        new_data_3 = list()
        # Only get some specific activites
        id_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 15, 24, 28]
        for d in data_3:
            if d["ID"] in id_list:
                new_data_3.append({
                    "date": convert_date(d["LocalDateTime"]),
                    "activity": get_activity_name(d["ID"]),
                    "rating": d["Category"]
                })

        # Composing the result by joining the two pieces of data
        df_2 = pd.DataFrame(new_data_2)
        df_3 = pd.DataFrame(new_data_3)
        df = pd.merge(df_2, df_3, on="date")
        df = df.pivot(index=["date", "max_uvr"], columns="activity", values="rating")
        df.reset_index(inplace=True)

        # Filter out activites to recommend/not-recommend
        raw_result = df.to_dict('records')
        for dt in raw_result:
            dt["excellent_activites"] = [act for act in dt.keys() if (act!="date" and dt[act] in ["Excellent", "Very Good"])]
            dt["poor_activites"] = [act for act in dt.keys() if (act!="date" and dt[act] in ["Poor"])]
        # Compose result data
        result = [
            {
                "suburb": suburb_name,
                "date": di["date"],
                "max_uvr": di["max_uvr"],
                "excellent_activites": check_activites(di["excellent_activites"]),
                "poor_activites": check_activites(di["poor_activites"]),
            } 
            for di in raw_result
        ]
        # Clean up memory
        raw_result = None

    # If error occurs then return default data
    except Exception:
        result = list()
        to_day = datetime.datetime.today()
        for d in range(0, 5):
            result.append({
                "suburb": suburb_name,
                "date": convert_date(to_day + datetime.timedelta(days=d)),
                "max_uvr": "Unkown",
                "excellent_activites": ["Stay Home"],
                "poor_activites": ["Go Out"],
            })
    # Always return data instead of error
    finally:
        return str(result)
    

# API to get next schedule for 1 chosen day (Iteration 3)
@app.route('/forecast_1day_i3')
def forecast_1day_i3():
    day = request.args.get('day')
    postcode = request.args.get('postcode')
    
    # Get coordinates from database
    PARAMS = find_coordinate(postcode)[0]
    PARAMS["dt"] = str(day + "T00:00:00.000Z")
    suburb_info = find_coordinate(postcode)[1]
    
    # Get data
    try:
        # Send API request to AccuWeather to get activities
        req = requests.get(url=OPENUV_URL_FORECAST, params=PARAMS, headers={"x-access-token": get_api_key()})
        data = json.loads(req.text)["result"]

        raw_result = [
            {
                "uvr": evaluate_uvr_i3(rd["uv"]),
                "timestamp": convert_to_AUS(rd["uv_time"])
            } 
            for rd in data
        ]
        get_item = operator.itemgetter("uvr")
        intervals = [ list(g) for _,g in itertools.groupby(raw_result, get_item) ]
        intervals = [ itv for itv in intervals if itv[0]["uvr"]!="H" ]

        result = {
            "suburb": suburb_info["name"],
            "low_uv": list(),
            "moderate_uv": list()
        }
        for itv in intervals:
            # Round the start time of the interval down
            start_time = str(itv[0]["timestamp"])
            start_time = round_minute(start_time, forward=False)

            # Round the end time of the interval up
            end_time = str(itv[-1]["timestamp"])
            end_time = round_minute(end_time, forward=True)
            
            # Classify intervals into Low and Normal UVR
            if itv[0]["uvr"] == "L":
                result["low_uv"].append("From " + start_time + " To " + end_time)
            else: 
                result["moderate_uv"].append("From " + start_time + " To " + end_time)

    # If error occurs then return default data
    except Exception:
        result = {
            "suburb": suburb_info["name"],
            "low_uv": list(),
            "moderate_uv": list()
        }
    # Always return data instead of error
    finally: 
        return str(result)


# API to get current UVR for 10 most crowded suburbs in Melbourne (Iteration 3)
@app.route('/uvr_inner_suburbs_i3')
def uvr_inner_suburbs_i3():
    # 18 most crowded suburbs in Melbourne
    INNER_SUBURBS = ['3000', '3121', '3182', '3056', '3141',  
                    '3051', '3181', '3053', '3162', '3168']
    # Get the data
    try:
        # List of data to return
        result = list()

        # Get data for each postcode
        for postcode in INNER_SUBURBS:
            # Get coordinates from database
            PARAMS = find_coordinate(postcode)[0]
            suburb_info = find_coordinate(postcode)[1]
            
            # Send API request to OpenUV
            req = requests.get(url=OPENUV_URL_RECENT, params=PARAMS, headers={"x-access-token": get_api_key()})
            data = json.loads(req.text)
            
            # Compose result data
            result.append({
                'postcode': postcode,
                'suburb': suburb_info['name'],
                'UVR': data['result']['uv'],
                'max_UVR': data['result']['uv_max']
            })
    # Return defalut data if error occurs
    except Exception:
        result = [
            { 'postcode': '3000', 'suburb': 'MELBOURNE', 'UVR': 0, 'max_UVR': 6 }, 
            { 'postcode': '3121', 'suburb': 'BURNLEY', 'UVR': 0, 'max_UVR': 6 }, 
            { 'postcode': '3182', 'suburb': 'ST KILDA', 'UVR': 0, 'max_UVR': 6 }, 
            { 'postcode': '3056', 'suburb': 'BRUNSWICK', 'UVR': 0, 'max_UVR': 6 }, 
            { 'postcode': '3141', 'suburb': 'CHAPEL STREET NORTH', 'UVR': 0, 'max_UVR': 6 }, 
            { 'postcode': '3051', 'suburb': 'HOTHAM HILL', 'UVR': 0, 'max_UVR': 6 }, 
            { 'postcode': '3181', 'suburb': 'PRAHRAN', 'UVR': 0, 'max_UVR': 6 }, 
            { 'postcode': '3053', 'suburb': 'CARLTON', 'UVR': 0, 'max_UVR': 6 }, 
            { 'postcode': '3162', 'suburb': 'CAULFIELD', 'UVR': 0, 'max_UVR': 6 }, 
            { 'postcode': '3168', 'suburb': 'CLAYTON', 'UVR': 0, 'max_UVR': 6 }
        ]
    # Always return data instead of error
    finally:
        return str(result)


# --------------------------------------------------------------------------------------
# --------------------------- Start the main API application ---------------------------
# --------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run()
