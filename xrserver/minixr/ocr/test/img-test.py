from imageai.Detection import ObjectDetection
import os
import cv2
execution_path = os.getcwd()
print(execution_path)
detector = ObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath( os.path.join(execution_path , "models/yolov3.pt"))
detector.loadModel()
detections = detector.detectObjectsFromImage(input_image=os.path.join(execution_path , "demo.jpg"), output_image_path=os.path.join(execution_path , "demo1.jpg"), minimum_percentage_probability=30)

for eachObject in detections:
    print(eachObject["name"] , " : ", eachObject["percentage_probability"], " : ", eachObject["box_points"] )
    print("--------------------------------")
    x,y,w,h = eachObject["box_points"]
    t_img = cv2.imread(os.path.join(execution_path , "demo.jpg"))
    show_img = cv2.rectangle(t_img.copy(), (x, y), (w , h),(255,0,0),2)
    cv2.imshow("Input", show_img)
    cv2.waitKey(0)