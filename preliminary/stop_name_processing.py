'''
Please refer to the README of the preliminary folder for any information.

Run stop_name_processing.py with the following command in your terminal. You should be in the home directory. 
```
python -m preliminary.stop_name_processing  --file_path <json file> 
                                            --stop_key <key of stop names> 
                                            --stop_path <txt csv file with stops>
                                            --stop_name <name of column with stop names>
                                            --stop_code <name of column with stop codes>
                                            --output_name <name of output csv>
                                            (optional):
                                            --start <i>
```
'''

import json
import csv
import pandas as pd
import argparse
from google import genai
from personalconstants import GEMINI_API_KEY
import time

# parse the arguments
parser = argparse.ArgumentParser()
parser.add_argument('--file_path', default='data/delays/bus-delay-data.json')
parser.add_argument('--stop_key', default='Location')
parser.add_argument('--stop_path', default='data/TTC Routes and Schedules Data/stops.txt')
parser.add_argument('--stop_name', default='stop_name')
parser.add_argument('--stop_code', default='stop_code')
parser.add_argument('--output_name', default='preliminary/results.txt')
parser.add_argument('--start', default=0)



args = parser.parse_args()

# Load the data
with open(args.file_path, "r") as file:
    data = json.load(file)

unprocessed_stops_df = pd.DataFrame(data[args.stop_key])

stops_df = pd.read_csv(args.stop_path)

stop_data = stops_df[[args.stop_code, args.stop_name]]
stop_data = stop_data.to_csv(index=False)
unprocessed_stops = unprocessed_stops_df.to_csv(index=False)

# Create Prompt
standard_prompt = "You will be given 2 sets of information: \n\
        1) CSVs containing stop data, where the first column is the stop id, and the second column is its name;\n\
        2) A list of containing 10 names, which may be misspelled, concatenated, shortened, or anything in between, describing the stop names mentioned in the previous CSV.\n\
        Your response should be a CSV file with 10 rows where the first column is the corresponding value from the list (2),\
              the second column is the correct name,\
              and the third column is the stop code.\
              If you do not know what the correct name is, put NONE in the second and third column.\n\
        Ensure that you have checked all possible stops in the stop data list. DO NOT add additional annotations.\n"

full_response = ""

for i in range(args.start,len(unprocessed_stops)-10,10):

    curr_unprocessed_stops_csv = unprocessed_stops_df[i:i+11].to_csv(index = False)

    prompt = standard_prompt + "Information set 1:\n" + stop_data + "\n\nInformation set 2:\n" + curr_unprocessed_stops_csv
    
    try: 
        # Call Gemini
        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(
            model="gemini-1.5-flash", contents=prompt
        )
        print(response.text)
        full_response = full_response+"\n\n"+response.text

        with open(args.output_name, "a") as file:
            file.write(response.text)

        count = 0
    except:
        time.sleep(30) # try to wait until API calls are refreshed
        count+=1
        if count > 5:
            break

# Precautionary file
with open("results_full.txt", "w") as file:
    file.write(full_response) 

print(f'Processing stopped at index {i}. Please continue with additional argument --start <i>.')

# Note to self: we can also try to use fuzzywuzzy for fuzze string matching?