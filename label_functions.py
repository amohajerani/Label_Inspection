import datetime, os, pytesseract, cv2, sqlite3, numpy as np
from dateutil.relativedelta import relativedelta

def getTxt(imgPath): # this function gets the path to image and returns the text as a string
    img=cv2.imread(imgPath)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret,img_Binary = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    txt = pytesseract.image_to_string(img_Binary, config='--psm 1') # the psm of 1 is for automatic orientation
    return txt
def getPath(Path):# return the full path to the image
    files=[os.path.join(Path,f) for f in os.listdir(Path)]
    files=list(filter(os.path.isfile, files))
    files.sort(key=os.path.getctime, reverse=True)
    RemExtraFiles(files)
    return files[0]

def RemExtraFiles(files):# cleans the folder by removing old images
    for f in files[10:]:
        os.remove(f)
def disp(msg, imgPath):# display message on the image
    img=cv2.imread(imgPath)
    img = cv2.resize(img,(612, 816),fx=0, fy=0, interpolation = cv2.INTER_CUBIC)
    font                   = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (10,50)
    fontScale              = 1
    fontColor              = (0,0,255)
    lineType               = 3
    cv2.putText(img,msg, 
    bottomLeftCornerOfText, 
    font, 
    fontScale,
    fontColor,
    lineType)
    cv2.imshow("img",img)

# get the right message based on the outcome of analysis
def getMsg(isMfgDateCorr, isExpDateCorr, isDescCorr, isSymbCorr):
    if isMfgDateCorr and isExpDateCorr and isDescCorr and isSymbCorr == True:
        msg='Good label on '+str(d)
    elif isMfgDateCorr and isExpDateCorr and isDescCorr and isSymbCorr == False:
        msg='Bad label. Potentially blank label'
    elif isMfgDateCorr== False:
        msg="Bad label. Check Mfg date"
    elif isExpDateCorr==False:
        msg="Bad label. Check expiry date"
    elif isDescCorr==False:
        msg="Bad label. Check Product Description"
    elif isSymbCorr==False:
        msg="Bad label. Check Product symbol"
    return msg
class prod:# pull the infomration about product out of the database.
    def __init__(self, CatNum, c):
        catal=(CatNum,)
        c.execute("select * from products where catNum=?", catal)
        row=c.fetchone()
        self.descr=row[1]
        self.symbol=row[2]
        self.shelfLife=row[3]# in months
    
