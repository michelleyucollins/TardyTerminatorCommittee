To replicate the data extraction/construction process, you can do the following:

# Dependencies
Download all dependencies with 
```
pip -r data/requirments.txt
```

# News Sentiment
Run 
```
python data/newssent/NewsData.py --query TTC
python data/newssent/Sentiment.py --query TTC
```

# Maps
In order to run this API, you must have an API key to do this, generate one in [google api credentials page](https://console.cloud.google.com/apis/credentials).
