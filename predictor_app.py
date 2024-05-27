


from Utils import preprocess
from joblib import load
from flask import Flask, request, jsonify, render_template


model = load(r"E:\NLP\Final Project\Ahmed_Mostafa_attia_NLP_Project\ML\sentiment_analysis_ml_model.joblib")

labels = {'LY':'Lybia','LB':'Lebanon','EG':'Egypt','MA':'Morocco','SD':'Sudan'}


# Initialize the app
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('predictor.html')


@app.route('/predict', methods = ['POST'])
def predict():
    sentence = request.form['sentence']
    data = [preprocess(sentence)]
        
    if model.predict(data)[0] in labels.keys():
        pred = labels[model.predict(data)[0]]
        
    return render_template('predictor.html', 
                           answer = pred)

# Start the server, continuously listen to requests.
if __name__=="__main__":
    app.run(debug=False)
