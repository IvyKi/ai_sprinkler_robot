import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import datetime

# Load the fire data
fire_data_path = 'data001.xlsx'
fire_data = pd.read_excel(fire_data_path)

# Create a target variable indicating whether a fire occurred (1) or not (0)
fire_data['Fire_Occurred'] = 1

# Create a DataFrame with all possible valid dates in a year
valid_dates = []
for month in range(1, 13):
    for day in range(1, 32):
        try:
            # Check if the date is valid
            pd.Timestamp(f'2020-{month}-{day}')
            valid_dates.append((month, day))
        except ValueError:
            continue

# Create the DataFrame from valid dates
all_dates = pd.DataFrame(valid_dates, columns=['Month', 'Day'])

# Merge the fire data with this complete list of dates
all_dates = all_dates.merge(fire_data[['Month', 'Day', 'Fire_Occurred']],
                            on=['Month', 'Day'],
                            how='left').fillna(0)

# Separate features (Month and Day) and target variable (Fire_Occurred)
X = all_dates[['Month', 'Day']]
y = all_dates['Fire_Occurred']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a logistic regression model
logistic_model = LogisticRegression(random_state=42)
logistic_model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = logistic_model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
classification_report_output = classification_report(y_test, y_pred)


# Get today's month and day
today = datetime.date.today()
today_month = today.month
today_day = today.day

# Predict the probability of fire occurrence for today's date
today_fire_probability = 100*(logistic_model.predict_proba([[int(today_month), int(today_day)]])[0][1])

print(f'Fire Probability: {today_fire_probability:.2f}%')
