import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import datetime


class PredictProbability:
    def __init__(self, data_path):
        self.data_path = data_path
        self.fire_data = None
        self.all_dates = None
        self.x = None
        self.x_train = None
        self.x_test = None
        self.y = None
        self.y_pred = None
        self.y_train = None
        self.y_test = None
        self.probability = 0
        self.model = None

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
        """Train the logistic regression model.

            print(f"Model Accuracy: {accuracy * 100:.2f}%")
            print("Classification Report:\n", report)
        """
        self.x_train, self.x_test, self.y_train, self.y_test = self.prepare_data()
        self.model = LogisticRegression(random_state=42)
        self.model.fit(self.x_train, self.y_train)

        # Evaluate the model
        self.y_pred = self.model.predict(self.x_test)
        accuracy = accuracy_score(self.y_test, self.y_pred)
        report = classification_report(self.y_test, self.y_pred)

        return accuracy, report

    def predict_fire_probability(self, month, day):
        """Predict the probability of fire occurrence for a given date."""
        if not self.model:
            raise ValueError("Model is not trained yet. Call train_model() first.")

        self.probability = self.model.predict_proba([[month, day]])[0][1]
        return self.probability * 100

    def predict_today_fire_probability(self, month, day):
        """Predict the probability of fire occurrence for today's date."""
        return self.predict_fire_probability(month, day)


# Usage example
if __name__ == "__main__":
    # Initialize the FirePredictionModel class
    model = PredictProbability(data_path='data001.xlsx')

    # Load the data
    model.load_data()

    # Generate all valid dates and merge with fire data
    model.generate_all_dates()

    # Train the model
    model.train_model()

    today = datetime.datetime.today()
    # Predict fire probability for today's date
    today_fire_probability = model.predict_today_fire_probability(int(today.month), int(today.day))
    print(f"Fire Probability: {today_fire_probability:.2f}%")
