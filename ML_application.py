import pickle
from flask import Flask, request, render_template
import pandas as pd
import numpy as np
import datetime
import mysql.connector

# Initialize Flask application
application = Flask(__name__)  # Starting point of application
app = application

# Load the pre-trained model and scaler
model = pickle.load(open('regmodel.pkl', 'rb'))
initial_scalar = pickle.load(open('scaling.pkl', 'rb'))

def get_db_connection():
    """Establishes a connection to the MySQL database."""
    return mysql.connector.connect(
        host="db",  # MySQL container's hostname
        user="user",  # MySQL username
        password="azhar113",  # MySQL password
        database="Model_Logger",  # Database name
        auth_plugin="caching_sha2_password"
    )

@app.route('/')
def home():
    """Render the home page."""
    return render_template('home.html')  # Index page

@app.route('/predict', methods=['POST'])
def predict():
    """Handles prediction requests and logs the results."""
    try:
        # Extract data from the form
        data = [float(x) for x in request.form.values()]
        del data[9]  # Remove highly correlated 'TAX' value
        final_data = np.array(data).reshape(1, -1)
        
        # Make a prediction
        start_time = datetime.datetime.now()
        output = model.predict(final_data)
        final_output = round(output[0], 3)
        response_time = (datetime.datetime.now() - start_time).total_seconds()
        
        # Log the prediction to the database
        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                "INSERT INTO Log (Current_Date_Time, Input_Params, Output, Response_Time) VALUES (%s, %s, %s, %s)",
                (datetime.datetime.now(), str(final_data), str(final_output), response_time)
            )
            connection.commit()
        except Exception as e:
            print(f"Error logging data: {e}")
        finally:
            cursor.close()
            connection.close()

        # Render the result on the home page
        return render_template("home.html", prediction_text=f"Price of the house is approximately = ${final_output}")
    
    except Exception as e:
        return render_template("home.html", prediction_text=f"Error: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True)

