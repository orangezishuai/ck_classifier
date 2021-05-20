import cv2
 
cap = cv2.VideoCapture('rtsp://192.168.1.28/2')
 
# print(cap)
ret,frame = cap.read()
while True:
    ret,frame = cap.read()
    if not ret:
        break
    ret,frame = cap.read()
    cv2.imshow("current frame",frame)
    # cv2.imwrite('frame.jpg', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
cap.release()