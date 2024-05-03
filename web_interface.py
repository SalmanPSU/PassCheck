from flask import Flask, request, jsonify, render_template
import joblib
from data_preprocessing import password_features  # Ensure this function is properly defined.
import pandas as pd
app = Flask(__name__)

# Load the trained model
model = joblib.load('password_strength_model.joblib')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_password', methods=['POST'])
def check_password():
    password = request.form['password']
    features = password_features(password)
    # Ensure features are in a DataFrame (assuming 'password_features' returns a list or 1D array)
    if not isinstance(features, pd.DataFrame):
        features = pd.DataFrame([features],
                                columns=['length', 'unique_chars', 'digit_ratio', 'upper_ratio', 'lower_ratio',
                                         'special_ratio'])
    # Assuming features is already a DataFrame if you followed previous advice
    prediction = model.predict(features)[0]  # prediction should be an integer if your labels are encoded

    # Check prediction type and handle accordingly
    if isinstance(prediction, str):
        # If prediction is a string, find its index in the label list
        prediction_index = ["weak", "medium", "strong"].index(prediction)
    else:
        # If prediction is already an integer, use it directly
        prediction_index = prediction

    strength_label = ["weak", "medium", "strong"][prediction_index]
    return jsonify({'strength': strength_label})


if __name__ == '__main__':
    app.run(debug=True)  # Running in debug mode