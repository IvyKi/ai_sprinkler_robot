from ml_data11 import PredictProbability
from ml_data22 import PredictWeather
import datetime as dt

FILE_PATH = ['data001.xlsx', 'data002.xlsx']
TODAY = dt.datetime.now()


def predict_probability(file_path):
    ml_a = PredictProbability(file_path)
    ml_a.load_data()
    ml_a.generate_all_dates()
    ml_a.train_model()
    prob = ml_a.predict_today_fire_probability(int(TODAY.month), int(TODAY.day))

    return round(float(prob), 2)


def predict_weather(file_path):
    ml_b = PredictWeather(file_path)
    ml_b.load_data()
    ml_b.fill_missing_values()
    ml_b.calculate_average()
    pre_t, pre_h = ml_b.predict_today_weather(int(TODAY.month), int(TODAY.day))

    return round(float(pre_t), 2), round(float(pre_h), 2)


if __name__ == '__main__':
    probability = predict_probability(FILE_PATH[0])
    print(probability)

    temperature, humidity = predict_weather(FILE_PATH[1])
    print(temperature, humidity)
