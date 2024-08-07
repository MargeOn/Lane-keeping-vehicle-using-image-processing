import sys
import math
import cv2 as cv
import numpy as np
import serial
import time

# Mở cổng giao tiếp python với arduino
arduino = serial.Serial(port='COM5', baudrate=115200, timeout=0.1)
# Mở camera xe
cam = cv.VideoCapture(1)
window_name1 = 'Hinh goc'
window_name2 = 'Hinh xu ly'
while(True):
    # Lấy dữ liệu ảnh từ camera
    src = cam.read()[1]
    # Cho Hinh2 thành hình màu đen
    Hinh2=np.copy(src)
    Hinh2[:,:,:]=0
    # Phát hiện các cạnh trong ảnh
    dst = cv.Canny(src, 50, 200, None, 3)
    # Phát hiện các đường thẳng trong ảnh
    lines = cv.HoughLines(dst, 1, np.pi / 180, 150, None, 0, 0)
    # Khởi tạo các mảng rô1, theta1
    rho1=np.zeros(200)
    theta1=np.zeros(200)
    # Nếu các đường thẳng được tìm thấy, sẽ được lọc xem rằng có cần lấy những
    # đường thẳng cần thiết không
    if lines is not None:
        k=0;
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            # Các đường thẳng trong khoảng rô lớn hơn 0 và theta nhỏ hơn 0,76
            # hoặc các đường thẳng trong khoảng rô lớn hơn 0 và theta lớn hơn 1,57 thì lấy
            # và đưa vào mảng các giá trị  rô và theta
            if (rho>0 and theta<0.76) or (rho<0 and theta>1.57):
                rho1[k]=rho
                theta1[k]=theta
                k=k+1
        # Đưa mảng rô1, theta1 vào rô2, theta2         
        rho2=rho1[0:k]
        theta2=theta1[0:k]
        #print(rho2)
        # Vẽ đường thẳng lên hình màu đen Hinh2
        for i in range(0, len(rho2)):
            rho=rho2[i]
            theta=theta2[i]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
            pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
            cv.line(Hinh2, pt1, pt2, (255,255,255), 2)

    anh_Xam = cv.cvtColor(Hinh2, cv.COLOR_BGR2GRAY)
    (thresh, anh_NhiPhan) = cv.threshold(anh_Xam, 127, 255, cv.THRESH_BINARY)
     
    hang479=anh_NhiPhan[479,:]
    hang240=anh_NhiPhan[100,:]

    # Tìm điểm đường thẳng bên trái phía dưới camera
    Dem1=320
    while (Dem1>0) and (hang479[Dem1]==0):
        Dem1=Dem1-1
        kc1= 320- Dem1
    # Tìm điểm đường thẳng bên trái ở giữa camera
    Dem2=320
    while (Dem2>0) and (hang240[Dem2]==0):
        Dem2=Dem2-1        
        kc2= 320- Dem2
    # Tìm điểm đường thẳng bên phải phía dưới camera
    Dem3=320
    while (Dem3<639) and (hang479[Dem3]==0):
        Dem3=Dem3+1
        kc3= Dem3- 320
    # Tìm điểm đường thẳng bên phải ở giữa camera
    Dem4=320
    while (Dem4<639) and (hang240[Dem4]==0):
        Dem4=Dem4+1
        kc4= Dem4 - 320
        
    # Lấy khoảng cách trung bình giữa 2 đoạn thẳng
    tb12 = (kc1 + kc2)/ 2
    tb34 = (kc3 + kc4)/ 2
    # Nếu khoảng cách từ điểm ở giữa đến điểm bên phải của camera
    # lớn hơn khoảng cách bên trái của camera thì cho xe quay phải
    if tb12 < tb34 and (tb34-tb12) >= 5:
        print('Quay phải')
        arduino.write(b'1')
        time.sleep(0.1)
    # Nhưng nếu 2 khoảng cách không quá lớn thì xe đi thẳng
    if tb12 < tb34 and (tb34-tb12) < 5:
        print('Đi thẳng')
        arduino.write(b'3')
        time.sleep(0.1)
    # Nếu khoảng cách từ điểm ở giữa đến điểm bên phải của camera
    # nhỏ hơn khoảng cách bên trái của camera thì cho xe quay trái
    if tb12 > tb34 and (tb12-tb34) >= 5:
        print('Quay trái')
        arduino.write(b'2')
        time.sleep(0.1)
    # Nhưng nếu 2 khoảng cách không quá lớn thì xe đi thẳng
    if tb12 > tb34 and (tb12-tb34) < 5:
        print('Đi thẳng')
        arduino.write(b'3')
        time.sleep(0.1)    
        
    
    td1=(Dem1,479)
    td2=(Dem2,100)
    td3=(Dem3,479)
    td4=(Dem4,100)
    # Vẽ đường thẳng lên
    cv.line(src, td1, td2, (255,255,0), 2)
    cv.line(src, td3, td4, (255,255,0), 2)
    # hiển thị ảnh từ camera
    cv.imshow(window_name1, src)
    # hiển thị ảnh nhị phân Hinh2
    cv.imshow(window_name2, Hinh2) 
    # thoát vòng lặp xử lí ảnh 
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
# Đóng cổng serial
arduino.close()
# Tắt camera
cam.release()
cv.destroyAllWindows()
