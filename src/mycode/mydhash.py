#encoding:utf-8
import numpy as np
import cv2
#import video #Opencv Python自带的读取

help_message = '''
USAGE: opt_flow.py [<video_source>]

Keys:
 1 - toggle HSV flow visualization
 2 - toggle glitch

'''
def classify_pHash(image1,image2): 
    image1 = cv2.resize(image1,(32,32)) 
    image2 = cv2.resize(image2,(32,32)) 
    gray1 = cv2.cvtColor(image1,cv2.COLOR_BGR2GRAY) 
    gray2 = cv2.cvtColor(image2,cv2.COLOR_BGR2GRAY) 
 # 将灰度图转为浮点型，再进行dct变换 
    dct1 = cv2.dct(np.float32(gray1)) 
    dct2 = cv2.dct(np.float32(gray2)) 
 # 取左上角的8*8，这些代表图片的最低频率 
 # 这个操作等价于c++中利用opencv实现的掩码操作 
 # 在python中进行掩码操作，可以直接这样取出图像矩阵的某一部分 
    dct1_roi = dct1[0:8,0:8] 
    dct2_roi = dct2[0:8,0:8] 
    hash1 = getHash(dct1_roi) 
    hash2 = getHash(dct2_roi) 
    return Hamming_distance(hash1,hash2) 

def getHash(image): 
    avreage = np.mean(image) 
    hash = [] 
    for i in range(image.shape[0]): 
        for j in range(image.shape[1]): 
            if image[i,j] > avreage: 
                hash.append(1) 
            else: 
                hash.append(0) 
    return hash 
 
 
def Hamming_distance(hash1,hash2): 
    num = 0 
    for index in range(len(hash1)): 
        if hash1[index] != hash2[index]: 
            num += 1 
    return num 
 
def draw_flow(img, flow, step=16):
    h, w = img.shape[:2]
    y, x = np.mgrid[step/2:h:step, step/2:w:step].reshape(2,-1)#以网格的形式选取二维图像上等间隔的点，这里间隔为16，reshape成2行的array
    fx, fy = flow[y,x].T#取选定网格点坐标对应的光流位移
    lines = np.vstack([x, y, x+fx, y+fy]).T.reshape(-1, 2, 2)#将初始点和变化的点堆叠成2*2的数组
    lines = np.int32(lines + 0.5)#忽略微笑的假偏移，整数化
    vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    cv2.polylines(vis, lines, 0, (0, 255, 0))#以初始点和终点划线表示光流运动
    for (x1, y1), (x2, y2) in lines:
        cv2.circle(vis, (x1, y1), 1, (0, 255, 0), -1)#在初始点（网格点处画圆点来表示初始点）
    return vis

def draw_hsv(flow):
    h, w = flow.shape[:2]
    fx, fy = flow[:,:,0], flow[:,:,1]
    ang = np.arctan2(fy, fx) + np.pi#得到运动的角度
    v = np.sqrt(fx*fx+fy*fy)#得到运动的位移长度
    hsv = np.zeros((h, w, 3), np.uint8)#初始化一个0值空3通道图像
    hsv[...,0] = ang*(180/np.pi/2)#B通道为角度信息表示色调
    hsv[...,1] = 255#G通道为255饱和度
    hsv[...,2] = np.minimum(v*4, 255)#R通道为位移与255中较小值来表示亮度
    bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)#将得到的HSV模型转换为BGR显示
    return bgr

def warp_flow(img, flow):
    h, w = flow.shape[:2]
    flow = -flow
    flow[:,:,0] += np.arange(w)
    flow[:,:,1] += np.arange(h)[:,np.newaxis]
    res = cv2.remap(img, flow, None, cv2.INTER_LINEAR)#图像几何变换（线性插值），将原图像的像素映射到新的坐标上去
    return res

if __name__ == '__main__':
    import sys
    print help_message
    try: fn = sys.argv[1]
    except: fn = 0

    cam = cv2.VideoCapture('C:/test/pythonfiles/1min.mp4')#读取视频
    ret, prev = cam.read()#读取视频第一帧作为光流输入的当前帧֡
    #prev = cv2.imread('E:\lena.jpg')
    prevgray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)
    show_hsv = True
    show_glitch = True
    cur_glitch = prev.copy()
    ret1, img1 = cam.read()
    while True:
        ret, img = cam.read()#读取视频的下一帧作为光流输入的当前帧
        if ret == True:#判断视频是否结束
            if cv2.cv.WaitKey(10)==27:
                break
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray1= cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
            degree = classify_pHash(img1,img) 
            img1=img
            print degree 
            flow = cv2.calcOpticalFlowFarneback(prevgray, gray, 0.5, 3, 15, 3, 5, 1.2, 0)#Farnback光流法
            prevgray = gray#计算完光流后，将当前帧存储为下一次计算的前一帧
            
            cv2.imshow('flow', draw_flow(gray, flow))
            if show_hsv:
                cv2.imshow('flow HSV', draw_hsv(flow))
            if show_glitch:
                cur_glitch = warp_flow(cur_glitch, flow)
                cv2.imshow('glitch', cur_glitch)
    
            ch = 0xFF & cv2.waitKey(5)
            if ch == 27:
                break
            if ch == ord('1'):
                show_hsv = not show_hsv
                print 'HSV flow visualization is', ['off', 'on'][show_hsv]
            if ch == ord('2'):
                show_glitch = not show_glitch
                if show_glitch:
                    cur_glitch = img.copy()
                print 'glitch is', ['off', 'on'][show_glitch]
        else:
            break
    cv2.destroyAllWindows()             

