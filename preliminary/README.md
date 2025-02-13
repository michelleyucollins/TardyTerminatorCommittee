# Folder for preliminary Data Analysis

## stop_name_processing.py
Python script which utilizes Gemini API calls to process stop names. 

### Why? - On Bus delay data
Observations of unique bus delay locations from preprocessed data (see "./data/delays/bus-delay-data.json") indicates an exorbant number of typos present, especially when compared to route station names in "data/TTC Routes and Schedules Data/stops.txt" (retrieved from https://open.toronto.ca/dataset/ttc-routes-and-schedules/). These files are pushed to github in a zip folder as they are very large. They are in the gitignore.

Further processing (textual) is necessary for ease of analysis in future steps. As texts must be done in a 1-1 manner, a LLM processing method would be used, aligned with that as described in Lecture #10 with Gemini 2.0 Flash. 

### How to use
This file utilizes Gemini 2.0 Flash, a free LLM API to perform textual processing. In order to use this file, or any similar textual processing files with Gemini in this repository, please first go through this API guide for Gemini: https://ai.google.dev/gemini-api/docs/quickstart?lang=python. Please ensure that you have your own API key stored in ./personalconstants.py as "GEMINI_API_KEY". You must have a google account in order to be able to replicate any API calls in this repository as we utilize a variety of Google Libraries.

./personalconstants.py is ignored by git and should look like this and should be in your home repository.
```
GEMINI_API_KEY = "<YOUR GEMINI API KEY>"
```

Then, please run stop_name_processing.py with the following command in your terminal. You should be in the home directory. 
```
python -m preliminary.stop_name_processing  --file_path <json file> 
                                            --stop_key <key of stop names> 
                                            --stop_path <txt csv file with stops>
                                            --stop_name <name of column with stop names>
                                            --stop_code <name of column with stop codes>
                                            --output_name <name of output csv>
```





