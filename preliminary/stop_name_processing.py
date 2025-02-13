'''
Please refer to the README of the preliminary folder for any information.

Run stop_name_processing.py with the following command in your terminal. You should be in the home directory. 
```
python -m preliminary.stop_name_processing.py --file_name <file name of desired csv>
```
'''

import json
import csv
import argparse
from google import genai
from personalconstants import GEMINI_API_KEY

parser = argparse.ArgumentParser()
parser.add_argument('--file_name', default='bus-delay.csv')
args = parser.parse_args()

client = genai.Client(api_key=GEMINI_API_KEY)
response = client.models.generate_content(
    model="gemini-2.0-flash", contents="Explain how AI works"
)
print(response.text)