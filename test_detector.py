import dlib
import cv2
import imutils
import threading
import serial
from imutils.video import WebcamVideoStream
from imutils.video import FPS

SERIAL_DEVICE = '/dev/ttyACM0'
#
ser = serial.Serial(SERIAL_DEVICE, 9600)

webcam = WebcamVideoStream(src=int(1)).start()
fps = FPS().start()

print 'cam started...'

cond = False


class CaptureThread(threading.Thread):
    def __init__(self, ):
        threading.Thread.__init__(self)
        self.runable = True

    def run(self):
        global cond
        while self.runable:
            data = ser.readline(1).strip()
            if data == 'S':
                cond = True
            print data


capture_thread = CaptureThread()
capture_thread.start()

# load the detector
squ = dlib.simple_object_detector('model/squ_detector.svm')
tri = dlib.simple_object_detector('model/tri_detector.svm')
try:
    cir = dlib.simple_object_detector('model/cir_detector.svm')
except Exception as e:
    print e
try:
    hexa = dlib.simple_object_detector('model/hex_detector.svm')
except Exception as e:
    print e
print 'model loaded..'

# loop over the testing images
while True:
    # for testingPath in paths.list_images(args["testing"]):
    # load the image and make predictions

    image = webcam.read()
    image = imutils.resize(image, width=400)
    # orig = image.copy()

    nimage = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    boxes1 = squ(nimage)
    boxes2 = tri(nimage)
    # boxes3 = cir(nimage)
    # boxes4 = hexa(nimage)
    for b in boxes1:
        print 'squ'
        (x, y, w, h) = (b.left(), b.top(), b.right(), b.bottom())
        cv2.putText(image, 'square', (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN, 1.2, (0, 255, 0), 2)
        cv2.rectangle(image, (x, y), (w, h), (0, 255, 0), 2)
    for b in boxes2:
        print 'tri'
        (x, y, w, h) = (b.left(), b.top(), b.right(), b.bottom())
        cv2.putText(image, 'triangle', (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN, 1.2, (0, 255, 0), 2)
        cv2.rectangle(image, (x, y), (w, h), (0, 255, 0), 2)
    '''
    for b in boxes3:
        print 'cir'
        (x, y, w, h) = (b.left(), b.top(), b.right(), b.bottom())
        cv2.putText(image, 'circle', (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN, 1.2, (0, 255, 0), 2)
        cv2.rectangle(image, (x, y), (w, h), (0, 255, 0), 2)
    for b in boxes4:
        print 'hex'
        (x, y, w, h) = (b.left(), b.top(), b.right(), b.bottom())
        cv2.putText(image, 'hex', (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN, 1.2, (0, 255, 0), 2)
        cv2.rectangle(image, (x, y), (w, h), (0, 255, 0), 2)
    '''
    if cond:
        print 'cond true'

        if len(boxes1) > 0:
            ser.write('L')
            cond = False
        if len(boxes2) > 0:
            ser.write('R')
            cond = False
        '''
        if len(boxes3)>0:
            ser.write('R')
            cond = False
        if len(boxes4)>0:
            ser.write('L')
            cond = False
        '''
    cv2.imshow("Image", image)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break
    fps.update()
# cv2.waitKey(0)
