# TardyTerminatorCommittee
Using ML to extract insights in transit delays

## Some setup
Our repository Gemini 2.0 Flash, a free LLM API to perform textual processing. In order to use any textual processing files with Gemini in this repository, please first go through this API guide for Gemini: https://ai.google.dev/gemini-api/docs/quickstart?lang=python. Please ensure that you have your own API key stored in ./personalconstants.py as "GEMINI_API_KEY". You must have a google account in order to be able to replicate any API calls in this repository as we utilize a variety of Google Libraries.

./personalconstants.py is ignored by git and should look like this and should be in your home repository.
```
GEMINI_API_KEY = <YOUR GEMINI API KEY>
```