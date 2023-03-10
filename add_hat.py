import numpy as np 
import cv2
import dlib


def add_hat(img,hat_img):

    r,g,b,a = cv2.split(hat_img) 
    rgb_hat = cv2.merge((r,g,b))

    cv2.imwrite("hat_alpha.jpg",a)



    # gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)  

    # face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")                       
    # faces = face_cascade.detectMultiScale(gray,1.05,3,cv2.CASCADE_SCALE_IMAGE,(50,50))




    predictor_path = "shape_predictor_5_face_landmarks.dat"
    predictor = dlib.shape_predictor(predictor_path)  


    detector = dlib.get_frontal_face_detector()


    dets = detector(img, 1)


    if len(dets)>0:  
        for d in dets:
            x,y,w,h = d.left(),d.top(), d.right()-d.left(), d.bottom()-d.top()
            # x,y,w,h = faceRect  
            # cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2,8,0)


            shape = predictor(img, d)
            # for point in shape.parts():
            #     cv2.circle(img,(point.x,point.y),3,color=(0,255,0))

            # cv2.imshow("image",img)
            # cv2.waitKey()  

            point1 = shape.part(0)
            point2 = shape.part(2)


            eyes_center = ((point1.x+point2.x)//2,(point1.y+point2.y)//2)

            # cv2.circle(img,eyes_center,3,color=(0,255,0))  
            # cv2.imshow("image",img)
            # cv2.waitKey()

            factor = 1.5
            resized_hat_h = int(round(rgb_hat.shape[0]*w/rgb_hat.shape[1]*factor))
            resized_hat_w = int(round(rgb_hat.shape[1]*w/rgb_hat.shape[1]*factor))

            if resized_hat_h > y:
                resized_hat_h = y-1


            resized_hat = cv2.resize(rgb_hat,(resized_hat_w,resized_hat_h))


            mask = cv2.resize(a,(resized_hat_w,resized_hat_h))
            mask_inv =  cv2.bitwise_not(mask)


            dh = 0
            dw = 0

            # bg_roi = img[y+dh-resized_hat_h:y+dh, x+dw:x+dw+resized_hat_w]
            bg_roi = img[y+dh-resized_hat_h:y+dh,(eyes_center[0]-resized_hat_w//3):(eyes_center[0]+resized_hat_w//3*2)]


            bg_roi = bg_roi.astype(float)
            mask_inv = cv2.merge((mask_inv,mask_inv,mask_inv))
            alpha = mask_inv.astype(float)/255


            alpha = cv2.resize(alpha,(bg_roi.shape[1],bg_roi.shape[0]))
            # print("alpha size: ",alpha.shape)
            # print("bg_roi size: ",bg_roi.shape)
            bg = cv2.multiply(alpha, bg_roi)
            bg = bg.astype('uint8')

            cv2.imwrite("bg.jpg",bg)
            # cv2.imshow("image",img)
            # cv2.waitKey()


            hat = cv2.bitwise_and(resized_hat,resized_hat,mask = mask)
            cv2.imwrite("hat.jpg",hat)
            
            # cv2.imshow("hat",hat)  
            # cv2.imshow("bg",bg)

            # print("bg size: ",bg.shape)
            # print("hat size: ",hat.shape)


            hat = cv2.resize(hat,(bg_roi.shape[1],bg_roi.shape[0]))

            add_hat = cv2.add(bg,hat)
            # cv2.imshow("add_hat",add_hat) 


            img[y+dh-resized_hat_h:y+dh,(eyes_center[0]-resized_hat_w//3):(eyes_center[0]+resized_hat_w//3*2)] = add_hat


            # cv2.imshow("img",img )  
            # cv2.waitKey(0)  

            return img

   

hat_img = cv2.imread("hat2.png",-1)


img = cv2.imread("pics/girlfriend.jpg")
# img = cv2.imread("pics/elonmusk.jpg")
# img = cv2.imread("pics/tomCruise.jpg")
output = add_hat(img,hat_img)


cv2.imshow("output",output )  
cv2.waitKey(0)  
cv2.imwrite("output.jpg",output)
# import glob as gb 

# img_path = gb.glob("./images/*.jpg")

# for path in img_path:
#     img = cv2.imread(path)

#
#     output = add_hat(img,hat_img)

#
#     cv2.imshow("output",output )  
#     cv2.waitKey(0)  

cv2.destroyAllWindows()  