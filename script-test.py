#USAGE
#Submit a request via Python programmatically:
#python script-test.py

#this script tests the accuracy of the predicted labels (cat or dog) against the
#actual label from 25000 images of cats and dogs in a folder names all/train gotten
#from an open source dataset. The dataset is structured as 'cat.xxxx.jpg' or
#'dog.xxxx.jpg', where xxx is a number between 0 and 12499. Thus there are equal
#images of cats and dogs and the first part of the file name indicates whether
#it is a cat or a dog. This indication has been used to get the true labels (actual)
#while the API calls to predict_cat_or_dog_with_probability endpoint will be used to
#get the predicted labels. Finally we find the accuracy between the true and predicted labels.

import requests
import os
import numpy as np

KERAS_REST_API_URL = "http://localhost:5000/predict_cat_or_dog_with_probability"
#KERAS_REST_API_URL = "http://0.0.0.0:5000/predict_cat_or_dog"
def get_files(cats_dogs, files, classification, probabilities, predictions):
    path = 'all/train'
    folder = os.fsencode(path)
    total_files = 0
    for file in os.listdir(folder):
        #print(file)
        total_files = total_files + 1
        filename = os.fsdecode(file)
        #print(filename)
        files.append(path + "/" + filename)
        IMAGE_PATH = path + "/" + filename
        image = open(IMAGE_PATH, "rb").read()
        payload = {"image": image}
        r = requests.post(KERAS_REST_API_URL, files=payload).json()
        if r["success"]:
            # loop over the predictions and display them
            for (i, result) in enumerate(r["predictions"]):
                '''print("{}. {}: {:.4f}".format(i + 1, result["animal"],
                                              result["probability"]))'''
                probabilities.append(result["probability"])
                if (result["probability"] >= 0 and result["probability"] < 0.5):
                    predictions.append(0)
                elif (result["probability"] >= 0.5 and result["probability"] <= 1):
                    predictions.append(1)
                else:
                    continue
        if (filename.split('.')[0] == 'cat'):
            classification.append(0)
            cats_dogs[0].append(path + "/" + filename)
        elif (filename.split('.')[0] == 'dog'):
            classification.append(1)
            cats_dogs[1].append(path + "/" + filename)
        else:
            continue
        '''if(predictions[-1] != classification[-1]):
            print("not accurate...")
            print(classification[-1])
            print(predictions[-1])
            print(probabilities[-1])
            print(files[-1])'''
    return total_files


if __name__ == "__main__":
    cats = []
    dogs = []
    cats_dogs = [cats, dogs]
    classification = [] #0 for cat, 1 for dog
    files = []
    predictions = []
    probabilities = []
    total_files = get_files(cats_dogs, files, classification, probabilities, predictions)
    '''print(cats_dogs[0])
    print(cats_dogs[1])
    print(files)
    print(classification)
    print(len(cats_dogs[0]))
    print(len(cats_dogs[1]))
    print(total_files)
    print(len(cats_dogs[0]) + len(cats_dogs[1]) == total_files)
    print(len(files))
    print(len(classification))'''
    #img_path =
    '''print(classification)
    print(predictions)'''
    actual = np.array(classification)
    predicted = np.array(predictions)
    correct = (actual == predicted)
    accuracy = (correct.sum() / correct.size) * 100
    print("The final accuracy(in percentage) = %f" % accuracy)