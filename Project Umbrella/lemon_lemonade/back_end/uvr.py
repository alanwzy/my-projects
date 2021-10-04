from sqlalchemy import create_engine
import pandas as pd

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

# Create connection to DB
engine = create_engine(
    "mysql+mysqlconnector://{user_name}:{pwd}@{server_name}/{db_name}".format(
        user_name=db_info['user_name'],
        pwd=db_info['pwd'],
        server_name=db_info['server_name'],
        db_name=db_info['db_name']
    )
)

# Specify the headers
header_list = ["timestamp", "lat", "lng", 'uv_index']

# Read all CSV files
for i in range(2010,2021,1):
    data = pd.read_csv('UVR_data/uv-melbourne-{}.csv'.format(i), header=None, skiprows=1, names=header_list)

    # Convert timestamp to proper format
    data['timestamp'] = pd.to_datetime(data['timestamp'], format="%Y-%m-%d %H:%M:%S")

    # Extract Month and Year
    data['month'] = data['timestamp'].dt.month
    data['year'] = data['timestamp'].dt.year

    # Drop not-needed cols
    data = data.drop(['timestamp', 'lat', 'lng'], axis=1)
    data = pd.DataFrame(data.groupby(['month', 'year'])['uv_index'].mean())
    data = data.reset_index()

    # Export to sql
    data.to_sql('uvr', con=engine, if_exists = 'append', chunksize = 1000)
