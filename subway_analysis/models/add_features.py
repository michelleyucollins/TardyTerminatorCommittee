import pandas as pd
import os

terminal_stations = {
    'LINE 1' : ['VAUGHAN METROPOLITAN CENTRE STATION', 'FINCH STATION'],
    'LINE 2' : ['KENNEDY STATION', 'KIPLING STATION'],
    'LINE 4' : ['SHEPPARD-YONGE STATION', 'DON MILLS STATION'],
}

def is_rush_hour(row):
    if row['Day'] in ['Saturday', 'Sunday']:
        return False
    
    hour = row['Datetime'].split(' ')[1].split(':')[0]
    if hour in ['7', '8', '9', '16', '17', '18']:
        return True
    
    return False

def is_terminal_station(row):
    line = row['Line Number']
    if line == 'LINE 1 and LINE 2':
        line = 'LINE 1'
    if row['Station Name'] in terminal_stations[line]: 
        return True
    return False

def add_features(df):
    df['Is Rush Hour'] = df.apply(is_rush_hour, axis=1)
    df['Is Terminal Station'] = df.apply(is_terminal_station, axis=1)
    return df

if __name__ == '__main__':
    data_path = "../../data/delays/subway/cleaned_data"
    dest_path = "../data"
    # Loop through all files in the data directory
    for file in os.listdir(data_path):
        if file.endswith(".csv"):
            df = pd.read_csv(os.path.join(data_path, file))
            df = add_features(df)
            df.to_csv(os.path.join(dest_path, file), index=False)