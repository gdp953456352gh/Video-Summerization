import cv2.cv as cv

capture = cv.CaptureFromFile('C:/test/pythonfiles/1min.mp4')
width = int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH))
height = int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT))

gray = cv.CreateImage((width,height), cv.IPL_DEPTH_8U, 1)

background = cv.CreateMat(height, width, cv.CV_32F)
backImage = cv.CreateImage((width,height), cv.IPL_DEPTH_8U, 1)
foreground = cv.CreateImage((width,height), cv.IPL_DEPTH_8U, 1)
output = cv.CreateImage((width,height), 8, 1)

begin = True
threshold = 10

while True:
    
    frame = cv.QueryFrame( capture )
    
    cv.CvtColor(frame, gray, cv.CV_BGR2GRAY)
    
    if begin:
        cv.Convert(gray, background) #Convert gray into background format
        begin = False
    
    cv.Convert(background, backImage) #convert existing background to backImage
    
    cv.AbsDiff(backImage, gray, foreground) #Absdiff to get differences
    
    cv.Threshold(foreground, output, threshold, 255, cv.CV_THRESH_BINARY_INV)
    
    cv.Acc(foreground, background,output) #Accumulate to background
    
    cv.ShowImage("Output", output)
    cv.ShowImage("Gray", gray)
    c=cv.WaitKey(1)
    if c==27: #Break if user enters 'Esc'.
        break