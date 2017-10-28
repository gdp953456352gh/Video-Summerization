#encoding:utf-8
import cv2.cv as cv
import cv2
import numpy as np

def draw_flow(img, flow, step=16):
    h, w = img.shape[:2]
    y, x = np.mgrid[step/2:h:step, step/2:w:step].reshape(2,-1)
    fx, fy = flow[y,x].T#ȡѡ������������Ӧ�Ĺ���λ��
    lines = np.vstack([x, y, x+fx, y+fy]).T.reshape(-1, 2, 2)#����ʼ��ͱ仯�ĵ�ѵ���2*2������
    lines = np.int32(lines + 0.5)#����΢Ц�ļ�ƫ�ƣ�������
    vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    cv2.polylines(vis, lines, 0, (0, 255, 0))#�Գ�ʼ����յ㻮�߱�ʾ�����˶�
    for (x1, y1), (x2, y2) in lines:
        cv2.circle(vis, (x1, y1), 1, (0, 255, 0), -1)#�ڳ�ʼ�㣨����㴦��Բ������ʾ��ʼ�㣩
    return vis


capture=cv.CaptureFromFile('C:/test/pythonfiles/1min.mp4')

frame1 = cv.QueryFrame(capture)
frame1gray = cv.CreateMat(frame1.height, frame1.width, cv.CV_8U)
cv.CvtColor(frame1, frame1gray, cv.CV_RGB2GRAY)

res = cv.CreateMat(frame1.height, frame1.width, cv.CV_8U)

frame2gray = cv.CreateMat(frame1.height, frame1.width, cv.CV_8U)

w= frame2gray.width
h= frame2gray.height
nb_pixels = frame2gray.width * frame2gray.height

while True:
    frame2 = cv.QueryFrame(capture)
    cv.CvtColor(frame2, frame2gray, cv.CV_RGB2GRAY)

    cv.AbsDiff(frame1gray, frame2gray, res)
    cv.ShowImage("After AbsDiff", res)

    cv.Smooth(res, res, cv.CV_BLUR, 5,5)
    element = cv.CreateStructuringElementEx(5*2+1, 5*2+1, 5, 5,  cv.CV_SHAPE_RECT)
    cv.MorphologyEx(res, res, None, None, cv.CV_MOP_OPEN)
    cv.MorphologyEx(res, res, None, None, cv.CV_MOP_CLOSE)
    cv.Threshold(res, res, 10, 255, cv.CV_THRESH_BINARY_INV)
#     prevgray = cv2.cvtColor(frame1gray, cv2.COLOR_BGR2GRAY)
#     nowgray == cv2.cvtColor(frame1gray, cv2.COLOR_BGR2GRAY)
    gh=np.asarray(frame2gray)
    prevgray = cv2.cvtColor(gh, cv2.COLOR_BGR2GRAY)
    flow = cv2.calcOpticalFlowFarneback(prevgray, prevgray, 0.5, 3, 15, 3, 5, 1.2, 0)#Farnback������
    cv2.imshow('flow', draw_flow(frame2gray, flow))
    cv.ShowImage("Image", frame2)
    cv.ShowImage("Res", res)

    #-----------
    nb=0
    for y in range(h):
        for x in range(w):
            if res[y,x] == 0.0:
                nb += 1
    avg = (nb*100.0)/nb_pixels
    #print "Average: ",avg, "%\r",
    if avg >= 50:
        print "need to be highlight !"
    #-----------


    cv.Copy(frame2gray, frame1gray)
    c=cv.WaitKey(1)
    if c==27: #Break if user enters 'Esc'.
        break