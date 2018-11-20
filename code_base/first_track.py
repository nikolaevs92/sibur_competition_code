import pandas as pd
import numpy as np
from fbprophet import Prophet
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import logging


logger = logging.getLogger(__name__)
logger.info("First track started")

coke_sample_submission = pd.read_csv('data/coke_sample_submission.csv', index_col="timestamp")
coke_target = pd.read_csv('data/coke_target.csv', index_col="timestamp")

# Prophet
data = coke_target.copy()
data['ds'] = data.index
data['y'] = data.target
forecast_data = coke_sample_submission.copy()
forecast_data['ds'] = forecast_data.index

model_fb = Prophet(
    daily_seasonality=True, growth='linear', weekly_seasonality=True, seasonality_mode='multiplicative')
model_fb.fit(data)

# ExponentialSmoothing
model_es = ExponentialSmoothing(
            coke_target[["target"]].squeeze(),
            trend = None,
            damped = False,
            seasonal = None,
            seasonal_periods = None
        ).fit()

# Predict
logger.info("First track train ended")
es_result = model_es.predict(
    start=pd.to_datetime(coke_sample_submission.index).values[0],
    end=pd.to_datetime(coke_sample_submission.index).values[-1]
    ).values
fb_result = model_fb.predict(forecast_data)["yhat"].values

# Веса взяты с валидации, как softmax(1/rmse_mode_fb, 1/rmse_model_es), 
WEIGHTS = [0.44751905, 0.55248095]
result_df = pd.DataFrame(
    data={
        "target": fb_result*WEIGHTS[0] + es_result*WEIGHTS[1], 
        "timestamp": coke_sample_submission.index
    }
)
result_df.to_csv("/output_data/first_track_result.csv", sep=',', index=False)
logger.info("First track ended")