from flask import Flask, request, render_template
import joblib
import numpy as np

# Initializing the Flask app
app = Flask(__name__)

# Loadng the trained model
model = joblib.load('model.joblib')

# Defining the home page route
@app.route('/')
def home():
    # Rendering the html main page for input
    return render_template('index.html')

# Defining the prediction route
@app.route('/predict', methods=['POST'])
def predict():
    # Getting the inputs from the form as a string and convert them to floats
    try:
        input_features = [float(x) for x in request.form.values()]
    except ValueError:
        return render_template('index.html', prediction_text='Please input valid numbers.')
    
    # Making a prediction using the model
    predicted_class = model.predict([input_features])[0]

    # Formatting the output text
    prediction_text = f'Predicted species: {predicted_class}'

    # Rendering the home page with the prediction result
    return render_template('index.html', prediction_text=prediction_text)

if __name__ == '__main__':
    # Running the app with debug for development purpose
    app.run(debug=True)