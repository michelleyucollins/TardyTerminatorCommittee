To replicate the data extraction/construction process, you can do the following:

# Dependencies
Download all dependencies with 
```
pip -r requirments.txt
```

# News Sentiment
Run 
```
python data/newssent/NewsData.py --query TTC
python data/newssent/Sentiment.py --query TTC
```

# Maps
In order to run this API, you must have an API key to do this, generate one in [google api credentials page](https://console.cloud.google.com/apis/credentials).

# TTC Routes and Schedules
You must open this zip folder locally to use this repository. This folder should NOT be pushed. It is in the gitignore file. 

# Weather Data 
Files are in csv format, and contain the  following information: 
- tavg: average tempearture (°C)
- tmin: min temperature (°C)
- tmax: max temperature (°C)
- prcp: total percipitation (mm)
- wdir: wind direction (TBD)
- wspd: wind speed (km/h)

File names: 
Station_name_MetrostatCode (Coordinates).csv
Source: [https://meteostat.net/en/](url)
