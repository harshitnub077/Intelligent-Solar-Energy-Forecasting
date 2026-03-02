from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

def run_forecast_pipeline(gen_df, weather_df):

    # Convert datetime
    gen_df['DATE_TIME'] = pd.to_datetime(gen_df['DATE_TIME'], errors='coerce')
    weather_df['DATE_TIME'] = pd.to_datetime(weather_df['DATE_TIME'], errors='coerce')

    # Merge
    df = pd.merge(gen_df, weather_df, on='DATE_TIME', how='inner')

    # Sort
    df = df.sort_values('DATE_TIME').reset_index(drop=True)

    # Time features
    df['hour'] = df['DATE_TIME'].dt.hour
    df['day'] = df['DATE_TIME'].dt.day
    df['month'] = df['DATE_TIME'].dt.month

    # Lag features
    df['ac_power_prev_1'] = df['AC_POWER'].shift(1)
    df['ac_power_prev_24'] = df['AC_POWER'].shift(24)
    df['ac_power_prev_2'] = df['AC_POWER'].shift(2)
    # df['ac_power_prev_3'] = df['AC_POWER'].shift(3)
    # df['ac_power_prev_48'] = df['AC_POWER'].shift(48)

    df['ac_power_roll_3'] = df['AC_POWER'].rolling(3).mean()
    # df['ac_power_roll_24'] = df['AC_POWER'].rolling(24).mean()

    # Drop NaNs from lags
    df = df.dropna().reset_index(drop=True)

    # Target
    y = df['AC_POWER']

    # Features
    X = df.drop(columns = [
        'DATE_TIME','AC_POWER',
        'DC_POWER','DAILY_YIELD','TOTAL_YIELD',
        'PLANT_ID','SOURCE_KEY','SOURCE_KEY_x','SOURCE_KEY_y','PLANT_ID_x','PLANT_ID_y'], errors='ignore')

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False
    )

    # Model
    model = RandomForestRegressor(n_estimators=200, max_depth=10,random_state=42)
    model.fit(X_train, y_train)

    # Predictions
    y_pred = model.predict(X_test)

    # Metrics
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    return model,mae, rmse, r2