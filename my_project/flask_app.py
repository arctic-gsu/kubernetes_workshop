from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

model = joblib.load('model.pkl')

@app.route('/predict',methods=['POST'])
def predict():
    data = request.get_json(force=True)
    prediction = model.predict([[700]])
    return jsonify({'prediction':prediction[0]})

if __name__ == '__main__':
    app.run(debug=True)
