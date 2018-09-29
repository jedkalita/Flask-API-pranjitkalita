#A Keras + deep learning REST API for predicting cat or dog

#The API handles images of any dimension, but converts it to (150x150x3) to predict
#in the given pre-trained Keras model.

Folder and files - 

all/train - 25000 images of cats and dogs in a folder names all/train gotten
#from an open source dataset. The dataset is structured as 'cat.xxxx.jpg' or
#'dog.xxxx.jpg', where xxx is a number between 0 and 12499. Thus there are equal
#images of cats and dogs and the first part of the file name indicates whether
#it is a cat or a dog. Files are not of size (150x150x3) but are converted.

dog.jpg - an image of a dog - File not of size (150x150x3) but are converted.
jemma.png - an image of a dog - File not of size (150x150x3) but are converted.
space_shuttle.png - an image of a space shuttle, i.e., neither a cat or a dog
 - File not of size (150x150x3) but are converted.

#Starting the Keras server

The Flask + Keras server can be started by running:

$ python server.py 
```
 Using TensorFlow backend.
* Loading Keras model, ResNet50 model. Starting server..Please wait until the server has started.
2018-09-28 19:50:13.162896: I tensorflow/core/platform/cpu_feature_guard.cc:141] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

You can now access the REST API via `http://0.0.0.0:5000` or `http://localhost:5000`.


#Submitting requests to the Keras server

Requests can be submitted via cURL:


API endpoint descriptions and results:

1. predict_cat_or_dog - POST method - 

find out if an image sent to the server is a dog or cat.

(a)
curl -X POST -F image=@all/train/cat.9.jpg 'http:/localhost:5000/predict_cat_or_dog'
Predicted animal is: Cat

(b)
curl -X POST -F image=@all/train/cat.9.jpg 'http:/0.0.0.0:5000/predict_cat_or_dog'
Predicted animal is: Cat

(c)
curl -X POST -F image=@all/train/dog.9.jpg 'http:/localhost:5000/predict_cat_or_dog'
Predicted animal is: Dog

(d)
curl -X POST -F image=@all/train/dog.9.jpg 'http:/0.0.0.0:5000/predict_cat_or_dog'
Predicted animal is: Dog

(e) 
curl -X POST -F image=@dog.jpg 'http:/localhost:5000/predict_cat_or_dog'
Predicted animal is: Dog

(f)
curl -X POST -F image=@dog.jpg 'http:/0.0.0.0:5000/predict_cat_or_dog'
Predicted animal is: Dog

(g)
curl -X POST -F image=@space_shuttle.png 'http:/localhost:5000/predict_cat_or_dog'
Predicted animal is: Cat

(h)
curl -X POST -F image=@space_shuttle.png 'http:/0.0.0.0:5000/predict_cat_or_dog'
Predicted animal is: Cat

(i)
curl -X POST -F image=@all/train/dog.991.jpg 'http:/0.0.0.0:5000/predict_cat_or_dog'
Predicted animal is: Cat

(j)
curl -X POST -F image=@all/train/cat.991.jpg 'http:/localhost:5000/predict_cat_or_dog'
Predicted animal is: Dog

(k)
curl -X POST -F image=@all/train/cat.7336.jpg 'http:/localhost:5000/predict_cat_or_dog'
Predicted animal is: Cat

(l)
curl -X POST -F image=@all/train/dog.7336.jpg 'http:/0.0.0.0:5000/predict_cat_or_dog'
Predicted animal is: Cat





2. predict_cat_or_dog_with_probability - POST method - 

find out if an image sent to the server is a dog or cat and also return the probability returned by the model in a son format.

(a)
curl -X POST -F image=@all/train/cat.9.jpg 'http:/localhost:5000/predict_cat_or_dog_with_probability'
{
  "predictions": [
    {
      "animal": "Cat", 
      "probability": 0.0765465721487999
    }
  ], 
  "success": true
}

(b)
curl -X POST -F image=@all/train/dog.9.jpg 'http:/0.0.0.0:5000/predict_cat_or_dog_with_probability'
{
  "predictions": [
    {
      "animal": "Dog", 
      "probability": 0.8986520767211914
    }
  ], 
  "success": true
}

(c)
curl -X POST -F image=@space_shuttle.png 'http:/0.0.0.0:5000/predict_cat_or_dog_with_probability'
{
  "predictions": [
    {
      "animal": "Cat", 
      "probability": 0.42874664068222046
    }
  ], 
  "success": true
}

(d)
curl -X POST -F image=@dog.jpg 'http:/0.0.0.0:5000/predict_cat_or_dog_with_probability'
{
  "predictions": [
    {
      "animal": "Dog", 
      "probability": 0.7259505987167358
    }
  ], 
  "success": true
}

(e)
curl -X POST -F image=@jemma.png 'http:/localhost:5000/predict_cat_or_dog_with_probability'
{
  "predictions": [
    {
      "animal": "Dog", 
      "probability": 0.7841367125511169
    }
  ], 
  "success": true
}




3. predict_cat_or_dog_with_probability_get - GET method - 

find out if an image sent to the server is a dog or cat and also return the probability returned by the model in a son format. Exactly the same as the POST method. I used this just to do some personal testing on POST vs GET.

(a)
curl -X GET -F image=@jemma.png 'http:/localhost:5000/predict_cat_or_dog_with_probability_get'
{
  "predictions": [
    {
      "animal": "Dog", 
      "probability": 0.7841367125511169
    }
  ], 
  "success": true
}

(b)
curl -X GET -F image=@space_shuttle.png 'http:/0.0.0.0:5000/predict_cat_or_dog_with_probability_get'
{
  "predictions": [
    {
      "animal": "Cat", 
      "probability": 0.42874664068222046
    }
  ], 
  "success": true
}

(c)
curl -X GET -F image=@all/train/dog.991.jpg 'http:/0.0.0.0:5000/predict_cat_or_dog_with_probability_get'
{
  "predictions": [
    {
      "animal": "Cat", 
      "probability": 0.36932313442230225
    }
  ], 
  "success": true
}

(d)
curl -X GET -F image=@all/train/cat.991.jpg 'http:/localhost:5000/predict_cat_or_dog_with_probability_get'
{
  "predictions": [
    {
      "animal": "Dog", 
      "probability": 0.6937900185585022
    }
  ], 
  "success": true
}


(e)
curl -X GET -F image=@all/train/cat.7336.jpg 'http:/localhost:5000/predict_cat_or_dog_with_probability_get'
{
  "predictions": [
    {
      "animal": "Cat", 
      "probability": 0.3184020519256592
    }
  ], 
  "success": true
}

(f)
curl -X GET -F image=@all/train/dog.7336.jpg 'http:/0.0.0.0:5000/predict_cat_or_dog_with_probability_get'
{
  "predictions": [
    {
      "animal": "Cat", 
      "probability": 0.31156980991363525
    }
  ], 
  "success": true
}



4. predict_with_confidence - POST method - 

We calculate how confident we are that a given image is a cat or a dog. If it is less confident, then we call another pre-trained model namely ResNet50 (by transforming the image to (240x240x3) to find out the top predictions of what object it could possibly be. This endpoint was designed to make the app more interesting and handle images that were neither cats not dogs, since the pre-trained cats and dogs model would return a predictor even for nonsensical images, e.g., space shuttle. This is also useful in cases where the model is not very confident if the prediction is actually consistent with if the passed image is a cat or a dog, since sometimes according to our heuristic, a cat may be classified as a dog or a cat or be very close to being classified as a dog. In that case, having another model to find out specifically what it could be might be useful.

(a)
curl -X POST -F image=@all/train/cat.9.jpg 'http:/localhost:5000/predict_with_confidence'
The animal is a Cat with high confidence of 84.69068%.

(b)
curl -X POST -F image=@all/train/dog.9.jpg 'http:/0.0.0.0:5000/predict_with_confidence'
The animal is a Dog with high confidence of 79.730415%.

(c)
curl -X POST -F image=@dog.jpg 'http:/0.0.0.0:5000/predict_with_confidence'
The animal is a Dog with low confidence of 45.19012%.
It is mostly one of the following with probabilities...
beagle:0.99017674
Walker_hound:0.0022487047
Brittany_spaniel:0.0011901348
pot:0.0011802911
Cardigan:0.0006831124

(d)
curl -X POST -F image=@jemma.png 'http:/localhost:5000/predict_with_confidence'
The animal is a Dog with high confidence of 56.827343%.

(e)
curl -X POST -F image=@space_shuttle.png 'http:/localhost:5000/predict_with_confidence'
The animal is a Cat with low confidence of 14.250671%.
It is mostly one of the following with probabilities...
space_shuttle:0.9971565
missile:0.00192375
projectile:0.0009182053
warplane:6.232783e-07
submarine:3.2804485e-07

(f)
curl -X POST -F image=@all/train/dog.991.jpg 'http:/0.0.0.0:5000/predict_with_confidence'
The animal is a Cat with low confidence of 26.135372%.
It is mostly one of the following with probabilities...
boxer:0.9826881
bull_mastiff:0.0090108095
Great_Dane:0.004051513
Rhodesian_ridgeback:0.0020681485
Doberman:0.0009144303

(g)
curl -X POST -F image=@all/train/cat.991.jpg 'http:/localhost:5000/predict_with_confidence'
The animal is a Dog with low confidence of 38.758003%.
It is mostly one of the following with probabilities...
Egyptian_cat:0.5515875
tabby:0.22625516
lynx:0.1015592
tiger_cat:0.02825449
Persian_cat:0.021254938

(h)
curl -X POST -F image=@all/train/cat.7336.jpg 'http:/localhost:5000/predict_with_confidence'
The animal is a Cat with low confidence of 36.319588%.
It is mostly one of the following with probabilities...
tabby:0.5804699
Egyptian_cat:0.3005333
tiger_cat:0.039164253
lynx:0.027976166
Siamese_cat:0.0036768347

(i)
curl -X POST -F image=@all/train/dog.7336.jpg 'http:/0.0.0.0:5000/predict_with_confidence'
The animal is a Cat with low confidence of 37.68604%.
It is mostly one of the following with probabilities...
German_shepherd:0.6873461
kelpie:0.15145586
Eskimo_dog:0.039455626
Border_collie:0.023808872
Siberian_husky:0.01033218

(j)
curl -X POST -F image=@jemma.png 'http:/0.0.0.0:5000/predict_with_confidence'
The animal is a Dog with high confidence of 56.827343%.





Programmatically (the following script calls the predict_cat_or_dog_with_probability endpoint to compare between an actual and predicted set of cats vs dogs classifications. The actual set is obtained from the folder all/train/ consisting of 25000 cats and dogs images with filenames cat{dog}.xxxx.jpg, the first part of the name implying whether it 
is a cat or a dog in actuality. The predicted labels from the model and the actual labels corresponding to them are compared and checked for accuracy in this script):

The script is described in detail in the headings portion of the file.

```
$ python script-test.py 
The final accuracy(in percentage) = 77.364000
```