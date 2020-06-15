import numpy as np
from PIL import Image
import tflite_runtime.interpreter as tflite
import cv2
import os  


class ImgClassifier:

    dir = ""
    img_size = 150
    spots = []
    labels =[]
    
    def imgToArray(self, img):
        path = self.dir+img
        img = cv2.imread(path, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (self.img_size, self.img_size))
        input_data = np.array(img, dtype=np.float32)
        input_data = np.expand_dims(input_data, 0)
        input_data = input_data/255
        return input_data
   

    def print(self):
        print ("green\topen\tyellow")
        
        for i in range (len(self.spots)):
            for j in self.spots[i]:
                for k in j:
                    print (round((k * 100),), end =" " + "%\t")
                print(self.labels[i])
            

    def __init__(self, dir):
        interpreter = tflite.Interpreter("/home/pi/ASABE/ASABE-2020/vision/imageclassifier/model_v2.tflite")
        interpreter.allocate_tensors()

        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()

        self.dir = dir
               
        for img in os.listdir(self.dir):
            
            input_data = self.imgToArray(img)
            img_name = img #unneeded
            self.labels.append(img)
            interpreter.set_tensor(input_details[0]["index"], input_data)
            interpreter.invoke()
            output_data = interpreter.get_tensor(output_details[0]['index'])
            
            self.spots.append(output_data.tolist())
