import cv2
cv=cv2
import numpy as np
import time
net = cv2.dnn.readNetFromDarknet("./minixr/ocr/test/yolov3.cfg", "./minixr/ocr/test/yolov3.weights")
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

def postprocess(frame, outs):
		frameHeight = frame.shape[0]
		frameWidth = frame.shape[1]
		classIds = []
		confidences = []
		boxes = []
		classIds = []
		confidences = []
		boxes = []
		for out in outs:
			for detection in out:
						scores = detection[5:]
						classId = np.argmax(scores)
						confidence = scores[classId]
						if confidence > confThreshold:
							center_x = int(detection[0] * frameWidth)
							center_y = int(detection[1] * frameHeight)
							width = int(detection[2] * frameWidth)
							height = int(detection[3] * frameHeight)
							left = int(center_x - width / 2)
							top = int(center_y - height / 2)
							classIds.append(classId)
							confidences.append(float(confidence))
							boxes.append([left, top, width, height])
    # Perform non maximum suppression to eliminate redundant overlapping boxes with
    # lower confidences.
		print(boxes)
		print(confidences)  
		indices = cv.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold) 
		for i in indices:
        #print(i)
        #i = i[0]
				box = boxes[i]
				left = box[0]
				top = box[1]
				width = box[2]
				height = box[3]
				drawPred(classIds[i], confidences[i], left, top, left + width, top + height)

def drawPred(classId, conf, left, top, right, bottom):
    # Draw a bounding box.
    cv.rectangle(frame, (left, top), (right, bottom), (0, 0, 255))
    label = '%.2f' % conf    
    # Get the label for the class name and its confidence
    if classes:
        assert(classId < len(classes))
        label = '%s:%s' % (classes[classId], label)
    #Display the label at the top of the bounding box
    labelSize, baseLine = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    top = max(top, labelSize[1])
    cv.putText(frame, label, (left, top), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))


confThreshold = 0.5 # Confidence threshold
nmsThreshold = 0.4  #Non-maximum suppression threshold
frame=cv2.imread("demo.jpg")
classesFile = "coco.names";
classes = None
with open(classesFile, 'rt') as f:
		classes = f.read().rstrip('\n').split('\n')

def getOutputsNames(net):
		# Get the names of all the layers in the network
		layersNames = net.getLayerNames()
		# Get the names of the output layers, i.e. the layers with unconnected outputs
		return [layersNames[i - 1] for i in net.getUnconnectedOutLayers()]
print(getOutputsNames(net))
# Remove the bounding boxes with low confidence using non-maxima suppression



blob = cv2.dnn.blobFromImage(frame, 1/255, (416, 416), [0,0,0], 1, crop=False)
t1=time.time()
net.setInput(blob)
outs = net.forward(getOutputsNames(net))
print(time.time()-t1)
postprocess(frame, outs)
t, _ = net.getPerfProfile()
label = 'Inference time: %.2f ms' % (t * 1000.0 / cv.getTickFrequency())
cv.putText(frame, label, (0, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))
cv2.imshow("result",frame)
