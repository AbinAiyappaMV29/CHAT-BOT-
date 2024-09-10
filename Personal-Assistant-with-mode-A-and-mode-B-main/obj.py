import cv2
import pyttsx3

text = pyttsx3.init()

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

classnames = []
classfile = 'coco.names'
with open(classfile, 'rt') as f:
    classnames = f.read().rstrip('/n').split('/n')

configpath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightpath = 'frozen_inference_graph.pb'

net = cv2.dnn_DetectionModel(weightpath, configpath)

net.setInputSize(320, 320)
net.setInputScale(1.0/127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

while True:
    ret, img = cap.read()
    classIds, confs, bbox = net.detect(img, confThreshold=0.5)
    print(classIds, bbox)

    if len(classIds) != 0:
        for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
            cv2.rectangle(img, box, color=(0, 25, 5, 0), thickness=2)
            cv2.putText(img, classnames[classId-1].upper(), (box[0]+10, box[1]+30),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

            ans = classnames[classId-1]
            rate = 40
            text.setProperty('rate', rate)
            text.say(ans)
            text.runAndWait()

    cv2.imshow('output', img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
