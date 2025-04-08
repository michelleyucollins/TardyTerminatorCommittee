# subway_analysis Folder TLDR
This folder contains all basic analysis and modelling points done on processed subway data.

## ./basic_analysis/time_analysis.ipynb
This file performs basic analysis on the subway delays based on their time. Multiple Linear Regression was used to establish a baseline model.

## ./basic_analysis/weather_analysis.ipynb
This file performs basic analysis on the subway delays based on the weather of the day the delay occured on. Multiple Linear Regression was used to establish a baseline model.

## ./models/add_features.py
Python file which adds features necessary for models

## ./models/weather_nn.ipynb
Basic Feed Forward Neural Network implemented for delays, with Weather of the day being the input and mean/count delays being the output. Conclusions: Some improvements to MSE, but still very high.

## ./models/LSTM_model.ipynb
LSTM model implemented to see if sequential patterns could be found within subway delays and the delay location. No successful results retrieved due to bias in data distribution/