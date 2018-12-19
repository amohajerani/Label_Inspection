import pytesseract
import cv2
import sqlite3
import csv
from matplotlib import pyplot as plt
import numpy as np

def condition_img(img):
    # Accept path to image and return cv2 object
    # that is black and white and cropped to size
    
    img_binary = binarize(img)
    img_cropped = crop(img_binary)
    img_filtered = cv2.medianBlur(img_cropped,11)
    return img_filtered

def txt(img_path):
    # Convert the text of the image to a string
  
    img = condition_img(img_path)
    txt = pytesseract.image_to_string(img, config='--psm 1') 
    return txt.upper()

def check_symb(img_path, template_path):
    # Check if the b/w template is in the color image
    # Return True is the res value is above threshold.
           
    img = condition_img(img_path)
    template = binarize(template_path)
    w, h = template.shape[::-1]
    
    res = cv2.matchTemplate(img,template,cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv2.rectangle(img,top_left, bottom_right, 0, 3)

    # Uncomment below to plot the image
    #plt.subplot(121),plt.imshow(res,cmap = 'gray')
    #plt.subplot(122),plt.imshow(img,cmap = 'gray')
    #plt.show()
    threshold = 0.7
    return max_val > threshold

def binarize(img_path):
    # Convert image to a cv2 binary file.
        
    img = cv2.imread(img_path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret,img_bi = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return img_bi

def crop(img):
    # crop cv2 image to w.h size
        
    y = 500
    x = 500
    h = 2000
    w = 1300
    img_cropped = img[y:y+h, x:x+w]    
    return img_cropped

def write_to_file(msg):
    # Print msg and write it to a scv file.

    with open("Report.csv", "a") as report:
        writer = csv.writer(report, lineterminator='\n')
        writer.writerow(msg)
        
    print("Date and time:      %s" %msg[0])
    print("Image:              %s" %msg[1])
    print("Inspection result:  %s" %msg[2])
    print("Cause(s) of fail:   %s" %msg[3])
    print('--------')

class db:
    # Return the description, code and shelf life (months)
    # of product associated with given cat#
    # from the databse db_path.

    def __init__(self, cat_num, db_path):
        conn = sqlite3.connect(db_path)
        c=conn.cursor()
        c.execute("select * from products where catNum=?", (cat_num,))
        
        row = c.fetchone()
        self.descr = row[1]
        self.code = row[2]
        self.shelf_life = row[3]
        
        conn.close()

    
