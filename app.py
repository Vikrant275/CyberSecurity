from flask import Flask,flash, render_template,jsonify, redirect, request, session, url_for
from framework.logger import logging
from framework.exception import MyException
import os,sys,json
import time
import pandas as pd
from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.pipeline.batch_prediction import PredictionPipeline

application =Flask(__name__)
app = application


@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else :
        return render_template('train_model.html')
@app.route('/train_model',methods=['GET'])
def train_model():
    with open('D:\\PythonProject3\\CyberSecurity\\networksecurity\\config\\models_json.json', 'r') as f:
        models = json.load(f)

    model_names = list(models.keys())
    project_info = {
        "name": "AI Training System",
        "dataset": "Custom Dataset",
        "version": "1.0",
        "status": "Ready for Training"
    }

    return render_template(
        'train_model.html',
        models=model_names,
        info=project_info
    )

# AJAX Training Endpoint
@app.route('/start_pipeline', methods=['POST'])
def start_pipeline():
    print("🚀 Training pipeline started...")
    try:
        model_training_artifact = TrainingPipeline().start_pipeline()
        return jsonify({
            "status": "success",
            'result':model_training_artifact
        })

    except Exception as e:
        logging.error(e)
        raise MyException(e,sys)

@app.route('/results_train')
def results_train():
    return render_template('results.html')


@app.route('/predict',methods=['POST','GET'])

def predict():
    if request.method == 'GET':
        return render_template("predict.html")
    else:
        try:

            data = pd.DataFrame([request.json])
            y_hat = PredictionPipeline(data).predict()
            print(y_hat)
            result = "🚨 Phishing Website" if y_hat > 1 else "✅ Legit Website"

            return jsonify({
                "status": "success",
                "prediction": result
            })

        except Exception as e:
            logging.error(e)
            raise MyException(e,sys)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)


