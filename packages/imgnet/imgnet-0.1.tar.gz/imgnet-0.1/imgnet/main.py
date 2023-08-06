import json

import yaml
from flask import Flask, render_template, request,jsonify
from flask_cors import CORS, cross_origin
from imgnet_engine.classification.imgnet_classification import trainEngine
#initializing flask app
from threading import Timer
import webbrowser
app=Flask(__name__)
CORS(app)

config_path="imgnet_config/classification.yaml"

@app.route('/',methods=['GET'])  # route to display the home page
def homePage():
    return render_template("home.html")

@app.route('/classificationInput',methods=['GET','POST'])
def classificationInput():
    '''
      Description: Here let's take input for image classification
    '''
    return render_template("classificationInput.html")


@app.route('/trainModel',methods=['GET','POST'])
def trainModel():
    '''
      Description: Here let's take input for image classification
    '''
    try:
        if request.method == 'POST':
            try:
                # Data config
                TRAINING_DATA_DIR = request.form['TRAINING_DATA_DIR']
                AUGMENTATION = request.form['AUGMENTATION']
                BATCHSIZE = int(request.form['BATCHSIZE'])

                # Model config
                MODEL_NAME = request.form['MODEL_NAME']
                FREEZE_ALL_LAYER = request.form['FREEZE_ALL_LAYER']
                OPTIMIZER = request.form['OPTIMIZER']
                EPOCHS = int(request.form['EPOCHS'])
                LOSSFUN = request.form['LOSSFUN']

                config = {
                    "TRAIN_DATA_DIR": TRAINING_DATA_DIR,
                    "AUGMENTATION": AUGMENTATION,
                    "BATCHSIZE": BATCHSIZE,
                    "MODEL_NAME": MODEL_NAME,
                    "EPOCHS": EPOCHS,
                    "FREEZE_ALL": FREEZE_ALL_LAYER,
                    "OPTIMIZER": OPTIMIZER,
                    "LOSS_FUNC": LOSSFUN

                }

                with open('imgnet_config/classification.yaml', 'w') as f:
                    print("Putting file inside classification,yaml")
                    yaml.dump(config, f)


                hist = trainEngine(config_path)

                return render_template('input_form.html', output=hist)

            except Exception as e:
                print('The Exception message is: ', e)
                return 'something is wrong'

    except Exception as e:
        print(e)

@app.route('/predictModel',methods=['GET','POST'])
def predictModel():
    '''
      Description: Here let's take input for image classification
    '''
    if request.method=='POST':
        print("Method called")
        data=request.form['MODEL_NAME']
        print(data)
        data=jsonify(data)
    else:
        return render_template("classificationInput.html")


def open_browser():
    webbrowser.open_new('http://127.0.0.1:8080/')

def start_app():
    Timer(1, open_browser).start()
    app.run(host="127.0.0.1", port=8080,debug=True)



if __name__ == "__main__":
    start_app()

