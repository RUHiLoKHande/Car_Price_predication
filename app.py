from flask import Flask, request, render_template
import joblib
import pandas as pd

app = Flask(__name__)

# Load the model
reg = joblib.load('model.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get input data from form
    car_name = request.form['car_name']
    year = int(request.form['year'])
    present_price = float(request.form['present_price'])
    kms_driven = int(request.form['kms_driven'])
    fuel_type = request.form['fuel_type']
    transmission = request.form['transmission']
    seller_type = request.form['seller_type']
    owner = int(request.form['owner'])

    # Prepare the input DataFrame
    input_data = pd.DataFrame([[car_name, year, present_price, kms_driven, fuel_type, transmission, seller_type, owner]],
                               columns=['Car_Name', 'Year', 'Present_Price', 'Kms_Driven', 'Fuel_Type', 'Transmission', 'Seller_Type', 'Owner'])

    # One-hot encode categorical features
    input_data = pd.get_dummies(input_data, drop_first=True)

    # Reindex to match training set
    input_data = input_data.reindex(columns=X_train.columns, fill_value=0)

    # Make prediction
    predicted_price = reg.predict(input_data)

    return f'Predicted Price: ₹{predicted_price[0]:.2f}'

if __name__ == '__main__':
    app.run(debug=True)
