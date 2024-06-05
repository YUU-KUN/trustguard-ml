import traceback
from flask import Flask, request, jsonify
import pickle
import numpy as np


app = Flask(__name__)

print("pickle version: ", pickle.format_version)

local_classifier = pickle.load(open('model.pkl', 'rb'))

def getPrediction():
    try:
        # amount, transaction time, location, customer_age, card_type, purchase_category
        request_data = request.get_json(force=True)
        amount = request_data['amount']
        type_number = request_data['type_number'] # 'CASH_OUT':1, 'PAYMENT':2, 'CASH_IN':3, 'TRANSFER':4, 'DEBIT':5
        oldbalanceOrg = request_data['oldbalanceOrg']
        newbalanceOrig = request_data['newbalanceOrig']
        oldbalanceDest = request_data['oldbalanceDest']
        newbalanceDest = request_data['newbalanceDest']
        # isFraud = request_data['isFraud']
        isFlaggedFraud = request_data['isFlaggedFraud']
        
        input_features = np.array([[amount, type_number, oldbalanceOrg, newbalanceOrig, oldbalanceDest, newbalanceDest, isFlaggedFraud]])
        prediction = local_classifier.predict(input_features)
        if prediction[0] == 0:
            result = "Not Fraud"
        else:
            result = "Fraud"

        response = jsonify({
            "prediction": prediction[0].tolist(),
            "result": result,
            "message": "This transaction is predicted as {}".format(result)
        })
        return response
    
    except:
        return jsonify({"trace": traceback.format_exc()})

@app.route('/')
def index():
    return "TrustShield Machine Learning API"

@app.route('/predict', methods=["POST"])
def predict():
    return getPrediction()

app.run(debug=True)