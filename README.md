# TardyTerminatorCommittee
Using ML to extract insights in transit delays

## Dependencies
Download all dependencies with 
```
pip -r requirments.txt
```

## Some setup
Our repository Gemini 2.0 Flash, a free LLM API to perform textual processing. In order to use any textual processing files with Gemini in this repository, please first go through this API guide for Gemini: https://ai.google.dev/gemini-api/docs/quickstart?lang=python. Please ensure that you have your own API key stored in ./personalconstants.py as "GEMINI_API_KEY". You must have a google account in order to be able to replicate any API calls in this repository as we utilize a variety of Google Libraries.

./personalconstants.py is ignored by git and should look like this and should be in your home repository.
```
GEMINI_API_KEY = "<YOUR GEMINI API KEY>"
```

## Directory Overview
TardyTerminatorCommittee/

./experimental # experimental items

./data # contains all data or data collection applications used for modelling

./preprocessing # contains preprocssing files

./bus_analysis # contains analysis on bus data

./subway_analysis # contains analysis on subway data

Further information can be found in the README files of each directory

## Contributors
Michelle Collins
Gary Liang 
Cindy Liu
