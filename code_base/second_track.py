import pandas as pd
import numpy as np
from fbprophet import Prophet
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import logging


logger = logging.getLogger(__name__)
logger.info("Second track started")

model_fb = Prophet()

reactor_pressure_sample_submission = pd.read_csv('data/reactor_pressure_sample_submission.csv', index_col="timestamp")
reactor_pressure_target = pd.read_csv('data/reactor_pressure_target.csv', index_col="timestamp")
sensors = pd.read_csv('data/sensors.csv', index_col="timestamp")

sensors.ffill(inplace=True)
sensors.fillna(sensors.mean(), inplace=True)
sensors.index = pd.to_datetime(sensors.index)
sensors = sensors.resample('H').mean()
reactor_pressure_target.index = pd.to_datetime(reactor_pressure_target.index)
reactor_pressure_target = reactor_pressure_target[['target']].resample('H').mean()

data = reactor_pressure_target.copy()
data['ds'] = data.index
data['y'] = data.target

for var in sensors.columns:
    model_fb.add_regressor(var, prior_scale=0.2)
    data[var] = sensors[var][:len(data)]

forecast_data = reactor_pressure_sample_submission.copy()
forecast_data['ds'] = forecast_data.index
for var in sensors.columns:
    forecast_data[var] = sensors[var][-len(forecast_data):]

model_fb.fit(data)
logger.info("Second track train ended")

forecast_result = model_fb.predict(forecast_data)

result_df = pd.DataFrame(data={"target": forecast_result["yhat"].values, "timestamp": reactor_pressure_sample_submission.index})
result_df.to_csv("/output_data/second_track_result.csv", sep=',', index=False)
logger.info("Second track ended")