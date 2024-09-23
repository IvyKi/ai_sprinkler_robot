import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import datetime as dt


class PredictProbability:
    def __init__(self, data_path):
        self.data_path = data_path
        self.fire_data = None
        self.all_dates = None
        self.x = None
        self.x_train = None
        self.x_test = None
        self.y = None
        self.y_pre = None
        self.y_train = None
        self.y_test = None
        self.probability = 0
        self.model = None
        self.accuracy = 0

    def load_data(self):
        """Load the fire data from an Excel file."""
        self.fire_data = pd.read_excel(self.data_path)
        self.fire_data['Fire_Occurred'] = 1

    def generate_all_dates(self):
        """Generate all valid dates for a year and merge with fire data."""
        valid_dates = []
        for month in range(1, 13):
            for day in range(1, 32):
                try:
                    pd.Timestamp(f'2020-{month}-{day}')
                    valid_dates.append((month, day))
                except ValueError:
                    continue

        all_dates_df = pd.DataFrame(valid_dates, columns=['Month', 'Day'])
        self.all_dates = all_dates_df.merge(
            self.fire_data[['Month', 'Day', 'Fire_Occurred']],
            on=['Month', 'Day'],
            how='left', validate="many_to_many").fillna(0)

    def prepare_data(self):
        """Prepare the features and target variable."""
        self.x = self.all_dates[['Month', 'Day']].values
        self.y = self.all_dates['Fire_Occurred'].values
        return train_test_split(self.x, self.y, test_size=0.2, random_state=42)

    def train_model(self):
        """Train the logistic regression model."""
        self.x_train, self.x_test, self.y_train, self.y_test = self.prepare_data()
        self.model = LogisticRegression(random_state=42)
        self.model.fit(self.x_train, self.y_train)

        # Evaluate the model
        self.y_pre = self.model.predict(self.x_test)
        self.accuracy = accuracy_score(self.y_test, self.y_pre)
        report = classification_report(self.y_test, self.y_pre)

        return self.accuracy, report

    def predict_fire_probability(self, month, day):
        """Predict the probability of fire occurrence for a given date."""
        if not self.model:
            raise ValueError("Model is not trained yet. Call train_model() first.")

        self.probability = self.model.predict_proba([[month, day]])[0][1]
        return self.probability * 100

    def get_all_probabilities(self):
        """Get fire probabilities for all 365 days of the year."""
        all_probabilities = []
        for month in range(1, 13):
            for day in range(1, 32):
                try:
                    pd.Timestamp(f'2020-{month}-{day}')  # Ensure it's a valid date
                    probability = self.predict_fire_probability(month, day)
                    all_probabilities.append({'Month': month, 'Day': day, 'Fire_Probability': probability})
                except ValueError:
                    continue
        return pd.DataFrame(all_probabilities)


if __name__ == "__main__":
    model = PredictProbability(data_path='data001.xlsx')

    model.load_data()
    model.generate_all_dates()
    model.train_model()

    today = dt.datetime.today()
    today_fire_probability = model.predict_fire_probability(int(today.month), int(today.day))

    all_probabilities_df = model.get_all_probabilities()
    output_path = 'fire_probabilities.xlsx'
    all_probabilities_df.to_excel(output_path, index=False)
