import cv2.cv as cv
capture = cv.CaptureFromFile('C:/test/pythonfiles/1min.avi')

nbFrames = int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_COUNT))
width = int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH))
height = int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT))
fps = cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FPS)
codec = cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FOURCC)

wait = int(1/fps * 3000/1) #Compute the time to wait between each frame query

duration = (nbFrames * fps) / 1000 #Compute duration

print 'Num. Frames = ', nbFrames
print 'Frame Rate = ', fps, 'fps'

writer=cv.CreateVideoWriter("C:/test/pythonfiles/test.avi", int(codec), int(fps), (width,height), 1) #Create writer with same parameters
cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_POS_FRAMES,80) #Set the number of frames

for f in xrange( nbFrames - 1380 ): #Just recorded the 80 first frames of the video

    frame = cv.QueryFrame(capture)

    print cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_POS_FRAMES)

    cv.WriteFrame(writer, frame)

    cv.WaitKey(wait)
del writer
writer=cv.CreateVideoWriter("C:/test/pythonfiles/test.avi", int(codec), int(fps), (width,height), 1) 
for f in xrange( nbFrames - 1500 ): #Just recorded the 80 first frames of the video

    frame = cv.QueryFrame(capture)

    print cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_POS_FRAMES)

    cv.WriteFrame(writer, frame)

    cv.WaitKey(wait)