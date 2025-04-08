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
    # As defined by the TTC
    if hour in ['6', '7', '8', '9', '15', '16', '17', '18', '19']:
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

def generate_ridership_mapping(datapath):
    rider_mapping = {}
    # Read ridership data
    for i in [1,2,4]:
        # Check if the file exists before reading
        if not os.path.exists(os.path.join(datapath, f'line_{i}_ridership.csv')):
            print(f"File line_{i}_ridership.csv not found in {datapath}.")
            continue
        # Read the ridership data for the line
        ridership = pd.read_csv(os.path.join(datapath, f'line_{i}_ridership.csv'))

        ridership = ridership.set_index('Station').T.to_dict('records')[0]
        # Create a mapping for the ridership data
        rider_mapping[f'LINE {i}'] = ridership

    rider_mapping['LINE 1 and LINE 2'] = rider_mapping['LINE 1'].copy()
    # Add ridership data to the main dataframe
    return rider_mapping

def add_ridership(df, mapping):
    df['Ridership'] = df.apply(lambda row: mapping[row['Line Number']][row['Station Name']], axis=1)
    return df

if __name__ == '__main__':
    data_path = "../../data/delays/subway/cleaned_data"
    dest_path = "../data"
    ridership_mapping = generate_ridership_mapping(dest_path)
    print(ridership_mapping)
    # Loop through all files in the data directory
    for file in os.listdir(data_path):
        if file.endswith(".csv"):
            df = pd.read_csv(os.path.join(data_path, file))
            df = add_features(df)
            df = add_ridership(df, ridership_mapping)
            # Save the modified dataframe to the destination path
            df.to_csv(os.path.join(dest_path, file), index=False)
