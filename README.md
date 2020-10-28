# optical-character-recognition
Optical character recognition project was created for of researching object detection problem, especially characters. Also it's interesting to find out whether it is possible to use a generated dataset for predicting real-world data.<br>

What has been done:
1. Created a module for generating characters (and saving bounding boxes)
2. Created a model (notebook) of EfficientDet for detecting a character
3. Created a model (notebook) of a simple CNN model using PyTorch.

What has been researched: <br>
1. Splitting detection-classification into seperate models is a more flexible solution, than just using an object-detection model, which predicts boxes with classes.
2. EfficientDet suits better, than yolov3 for this problem.
