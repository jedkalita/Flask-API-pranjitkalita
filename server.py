# USAGE
# Start the server:
# 	python server.py
# Submit a request via cURL:
# 	curl -X POST -F image=@all/train/cat.45.jpg 'http://localhost:5000/predict'
# Submit a request via Python:
#	python script-test.py

#imports
from keras.models import load_model
from keras.applications import ResNet50
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
from keras.applications import imagenet_utils
from PIL import Image
import numpy as np
import flask
import io


app = flask.Flask(__name__) #initialize our Flask application
model = None #initialize the given cats and dogs keras model
model_resnet50 = None #initialize the ResNet50 keras model

def load_models():
    # load the pre-trained Keras model (here we are using a model
    # pre-trained on ImageNet and provided by Keras, but you can
    # substitute in your own networks just as easily)
    global model
    global model_resnet50

    # model = ResNet50(weights="imagenet")
    model = load_model('cats_dogs_model.hdf5')
    model_resnet50 = ResNet50(weights="imagenet")

#load the image from the file in target into (150x150x3) and create 4 dimensions in the format the model
#expects
def load_image(img_path, show=False):
    img = image.load_img(img_path, target_size=(150, 150))
    img_tensor = image.img_to_array(img)                    #(height, width, channels)
    img_tensor = np.expand_dims(img_tensor, axis=0)         #(1, height, width, channels)
    # new dimension because the model expects 4 dimensions
    img_tensor /= 255.                                      #values in the range [0, 1]

    return img_tensor

#preprocessing the image for ResNet50 model input (240x240x3)
def prepare_image(image, target):
    # if the image mode is not RGB, convert it
    if image.mode != "RGB":
        image = image.convert("RGB")

    # resize the input image and preprocess it
    image = image.resize(target)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = imagenet_utils.preprocess_input(image)

    # return the processed image
    return image


#API endpoint - given an image, return a prediction whether it is a dog or cat - uses POST method
#returns a string indicating whether the predicted animal is a cat or a dog
@app.route("/predict_cat_or_dog", methods=["POST"])
def predict_cat_or_dog():
    data = {"success": False}
    if flask.request.method == "POST":
        if flask.request.files.get("image"):
            image = flask.request.files["image"]
            new_image = load_image(image)
            preds = model.predict(new_image)
            data["predictions"] = [] #to jsonify
            if preds > 0.5: #if it is closer to 1, then it is a dog
                result = 'Dog'
            else: #if it is closer to 0, then it is a cat
                result = 'Cat'

    return 'Predicted animal is: ' + result + '\n'


#API endpoint - given an image, return a prediction whether it is a dog or cat - uses POST method
#returns a JSON with name of predicted animal and probability (the value returned by the model)
@app.route("/predict_cat_or_dog_with_probability", methods=["POST"])
def predict_cat_or_dog_with_probability():
    data = {"success": False}
    if flask.request.method == "POST":
        if flask.request.files.get("image"):
            image = flask.request.files["image"]
            new_image = load_image(image)
            preds = model.predict(new_image)
            data["predictions"] = [] #to jsonify
            if preds > 0.5: #if it is closer to 1, then it is a dog
                result = 'Dog'
            else: #if it is closer to 0, then it is a cat
                result = 'Cat'

            data["success"] = True
            r = {"animal": result, "probability": float(preds[0][0])}
            data["predictions"].append(r)

    return flask.jsonify(data)

#API endpoint - given an image, return a prediction whether it is a dog or cat - uses GET method
#same as above in structure and functionality. Just checking GET vs POST.
@app.route("/predict_cat_or_dog_with_probability_get", methods=["GET"])
def predict_cat_or_dog_with_probability_get():
    data = {"success": False}
    if flask.request.method == "GET":
        if flask.request.files.get("image"):
            image = flask.request.files["image"]
            new_image = load_image(image)
            preds = model.predict(new_image)
            data["predictions"] = []
            if preds > 0.5: #if it is closer to 1, then it is a dog
                result = 'Dog'
            else: #if it is closer to 0, then it is a cat
                result = 'Cat'

            data["success"] = True
            r = {"animal": result, "probability": float(preds[0][0])}
            data["predictions"].append(r)

    return flask.jsonify(data)

#API endpoint - In this endpoint, we use the use a heuristic to calculate how sure we are if the
# prediction of the image is a dog or a cat. Then if we are more than 50% sure, then we display how
#confident we are. Otherwise, we call the ResNet50 model that has been trained on different varieties
#of objects to give the top predictions and return the statement.
@app.route("/predict_with_confidence", methods=["POST"])
def predict_with_confidence():
    data = {"success": False}
    if flask.request.method == "POST":
        if flask.request.files.get("image"):
            image = flask.request.files["image"]
            image2 = flask.request.files["image"].read()
            new_image = load_image(image)
            preds = model.predict(new_image) #value returned by our pre-trained Keras model
            data["predictions"] = []
            if preds > 0.5:
                result = 'Dog'
                surity = (abs(0.5 - preds) * 2.0) * 100.0 #calculate how sure you are based on how far
                #the prediction value is from 1
            else:
                result = 'Cat'
                surity = (abs(0.5 - preds) * 2.0) * 100.0 #calculate how sure you are based on how far
                #the prediction value is from 0

            data["success"] = True
            r = {"animal": result, "probability": float(preds[0][0])}
            data["predictions"].append(r)
        # return result + '\n'
        if (surity < 50): #if low confidence, ie less than 50% confidence
            statement = 'The animal is a ' + str(result) + ' with low confidence of ' + str(surity[0][0]) + '%.' + '\n'

            #then use the ResNet50 model to give the top predictions for what the object could be
            image2 = Image.open(io.BytesIO(image2)) #do the necessary preprocessing
            image2 = prepare_image(image2, target=(224, 224)) #target size is (224x224x3)
            predictions = model_resnet50.predict(image2) #call the ResNet50 model and get the predictions
            results = imagenet_utils.decode_predictions(predictions)
            statement = statement + 'It is mostly one of the following with probabilities...' + '\n'
            for (imagenetID, label, prob) in results[0]:
                statement = statement + str(label) + ':' + str(prob) + '\n'

        else:
            statement = 'The animal is a ' + str(result) + ' with high confidence of ' + str(surity[0][0]) + '%.' + '\n'
        return statement



# load the models and start the server
if __name__ == "__main__":
    print(("* Loading Keras model, ResNet50 model. Starting server.."
           "Please wait until the server has started."))
    load_models()
    app.run(host='0.0.0.0')