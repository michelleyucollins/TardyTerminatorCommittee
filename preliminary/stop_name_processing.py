'''
Please refer to the README of the preliminary folder for any information.

Run stop_name_processing.py with the following command in your terminal. You should be in the home directory. 
```
python -m preliminary.stop_name_processing  --type <gemini or fuzzy>
                                            --file_path <json file> 
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
from fuzzywuzzy import process

# parse the arguments
parser = argparse.ArgumentParser()
parser.add_argument('--type', default='fuzzy')
parser.add_argument('--file_path', default='data/delays/bus/bus-delay-data.json')
parser.add_argument('--stop_key', default='Location')
parser.add_argument('--stop_path', default='data/TTC Routes and Schedules Data/stop_names_unique.txt')
parser.add_argument('--stop_name', default='stop_name')
parser.add_argument('--stop_code', default='stop_code')
parser.add_argument('--output_name', default='preliminary/results.txt')
parser.add_argument('--start', default=0)

args = parser.parse_args()

def gemini_matching(unprocessed_stops_df, stop_data, args):
    # Create Prompt
    standard_prompt = "You are a station matching agent. \n\
            You will be given 3 sets of information: \n\
            1) Standard abbreviations; \n\
            2) CSVs containing actual stop names;\n\
            3) A list of containing 10 names, which may be misspelled, concatenated, shortened, or anything in between, describing the stop names mentioned in the previous CSV.\n\
            Your response should be a CSV file with 10 rows where the first column is the corresponding incorrect name from the list (3),\
                the second column is the correct name,\
                the third column is your confidence, on a scale of 0-100.\
                If you do not know what the correct name is, put NONE in the second and third column.\n\
            Ensure that you have checked all possible stops in the stop data list. You must return the best match. \n\
            DO NOT add additional annotations. DO NOT include headers.\n\n\
            Your output should be of the following format: \n\
            <incorrect stop name>, <correct stop name>, <confidence>\
            stc, Scarborough Town Centre, 100\n\
            kipling stn, Kipling Station, 100\n\
            papae stn, Pape Station, 90 "
    
    abbreviation_list = "Abbreviation, Actual\n\
        stc, Scarborough Town Center\n\
        <name> stn, <name> Street Station\n\
        york u, York University\n\
        main stn, Main Street Station"

    for i in range(int(args.start),len(unprocessed_stops_df)-10,10):

        curr_unprocessed_stops_csv = unprocessed_stops_df[i:i+10].to_csv(index = False)

        prompt = [standard_prompt, abbreviation_list, stop_data, curr_unprocessed_stops_csv]
        
        try: 
            # Call Gemini
            client = genai.Client(api_key=GEMINI_API_KEY)
            response = client.models.generate_content(
                model="gemini-2.0-flash", 
                contents=prompt
            )

            with open(args.output_name, "a") as file:
                file.write(response.text+"\n")

            count = 0
        except:
            time.sleep(30) # try to wait until API calls are refreshed
            count+=1
            if count > 10:
                break

    # If it forceably stops for any reason
    print(f'Processing stopped at index {i}. Please continue with additional argument --start <i>.')

def fuzzy_matching(unprocessed_stops_df, stop_data, args):
    stop_name_list = list(stop_data.iloc(axis=1)[1])
    bad_stop_data = list(unprocessed_stops_df.iloc(axis = 1)[0])

    # Make header
    prediction = ['bad_stop', 'confidence_1',  'stop_id_1', 'stop_name_1', 'confidence_2', 'stop_id_2', 'stop_name_2']
    try:
        with open(args.output_name, "w") as file:
            wr = csv.writer(file, quoting=csv.QUOTE_ALL)
            wr.writerow(prediction)
    except:
        print(f'Writing to file failed for stop {bad_stop}')


    for i in range(len(bad_stop_data)):
        bad_stop = bad_stop_data[i]
        try:
            if bad_stop == "stc":
                bad_stop = "Scarborough Town Centre"

            if "stn" in bad_stop:
                bad_stop = bad_stop[:bad_stop.index("stn")] + "station" + bad_stop[bad_stop.index("stn")+3:]

            if "york u " in bad_stop:
                bad_stop = bad_stop[:bad_stop.index("york u")] + "york university" + bad_stop[bad_stop.index("york u")+6:]
            # Get the top 2 most correlated items
            ans = process.extract(bad_stop, stop_name_list, limit=2)

            # Extract the stop information
            stop_1 = list(stop_data.iloc[stop_name_list.index(ans[0][0])])
            stop_2 = list(stop_data.iloc[stop_name_list.index(ans[1][0])])


            # We want to have the stop id, name and also confidence
            # Confidence is necessary to do manual fixes after 
            prediction = [bad_stop_data[i], ans[0][1], stop_1[0], stop_1[1],  ans[1][1], stop_2[0], stop_2[1]]

            try:
                with open(args.output_name, "a") as file:
                    wr = csv.writer(file, quoting=csv.QUOTE_ALL)
                    wr.writerow(prediction)
            except:
                print(f'Writing to file failed for stop {bad_stop_data[i]}')
        except:
            print(f"Process failed for {bad_stop_data[i]} at index {i}")
            prediction = [bad_stop_data[i], "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"]
            try:
                with open(args.output_name, "a") as file:
                    wr = csv.writer(file, quoting=csv.QUOTE_ALL)
                    wr.writerow(prediction)
            except:
                print(f'Writing to file failed for stop {bad_stop_data[i]}')
            continue


# Load the data
with open(args.file_path, "r") as file:
    data = json.load(file)

unprocessed_stops_df = pd.DataFrame(data[args.stop_key])

stops_df = pd.read_csv(args.stop_path)

# stop_data_df = stops_df[[args.stop_code, args.stop_name]]
stop_data = stops_df.to_csv(index=False)
unprocessed_stops = unprocessed_stops_df.to_csv(index=False)
print(len(unprocessed_stops_df))

#perform matching and export
if args.type == "gemini":
    gemini_matching(unprocessed_stops_df, stop_data, args)
else:
    fuzzy_matching(unprocessed_stops_df, stop_data_df, args)

# Note to self: we can also try to use fuzzywuzzy for fuzze string matching?