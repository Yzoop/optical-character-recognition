# optical-character-recognition
![alt text](https://github.com/Yzoop/optical-character-recognition/blob/main/proj_imgs/background.png?raw=true)
Optical character recognition project was created for of researching object detection problem, especially characters. Also it's interesting to find out whether it is possible to use a generated dataset for predicting real-world data.<br>

What has been done:
1. Created a module for generating characters (and saving bounding boxes). A training image looks like this:
<br> ![alt text](https://github.com/Yzoop/optical-character-recognition/blob/main/proj_imgs/012f7n1C8S.png)
<br>
2. Created a model (notebook) of EfficientDet for detecting a character
3. Created a model (notebook) of a simple CNN model using PyTorch.

What has been researched: <br>
1. Splitting detection-classification into seperate models is a more flexible solution, than just using an object-detection model, which predicts boxes with classes.
2. EfficientDet suits better, than yolov3 for this problem.

EfficientDet was compared to yolov3 on datasets with 10, 15, 38 classes of characters
 ![alt text](https://github.com/Yzoop/optical-character-recognition/blob/main/proj_imgs/yolov_vs_effdet.png)
