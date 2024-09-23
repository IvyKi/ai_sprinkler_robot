from ml_data11 import PredictProbability
from ml_data22 import PredictWeather


def predict_probability(file_path, month, day):
    ml_a = PredictProbability(file_path)
    ml_a.load_data()
    ml_a.generate_all_dates()
    ml_a.train_model()
    prob = ml_a.predict_fire_probability(month, day)

    return round(float(prob), 2)


def predict_weather(file_path, month, day):
    ml_b = PredictWeather(file_path)
    ml_b.load_data()
    ml_b.fill_missing_values()
    ml_b.calculate_average()
    pre_t, pre_h = ml_b.predict_today_weather(month, day)

    return round(float(pre_t), 2), round(float(pre_h), 2)
