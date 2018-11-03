import datetime, os, pytesseract, cv2, sqlite3, numpy as np
from dateutil.relativedelta import relativedelta
import label_functions as f
Path="C:\\Users\\username\\Desktop\\Images" # this is the folder containing images
dbPath="C:\\Users\\username\\Desktop\\prodDB.db" # path to product database
conn = sqlite3.connect(dbPath)
c=conn.cursor()
imgPath=f.getPath(Path)
txt=(f.getTxt(imgPath)).upper()
# check manufacturing date
d=datetime.datetime.now()
TodayDate="%(yr)s-%(mon)s-%(day)s" %{'yr':d.year, 'mon':d.month, 'day':d.day}
isMfgDateCorr= txt.find(TodayDate)!=-1 # if today's date is not in the text, it returns -1
try:#Identify the product catalog number
    CatNumIndex=txt.index("515")
    CatNum=txt[CatNumIndex:CatNumIndex+6]
except:
    msg='''No cat# starting with 515'''
    f.disp(msg, imgPath)
prodInfo=f.prod(CatNum, c)# get the attributes of the product from database
expDate=d+relativedelta(months=+prodInfo.shelfLife) # calculate expiry date as datetime object
ExpDate="%(yr)s-%(mon)s-%(day)s" %{'yr':expDate.year, 'mon':expDate.month, 'day':expDate.day}# convert to YYYY-MM-DD
isExpDateCorr= txt.find(ExpDate) !=-1# check if expiry date is correct
isDescCorr=txt.find(prodInfo.descr) !=-1# check if catNum matches the product description
isSymbCorr=txt.find(prodInfo.symbol) !=-1# check if catNum matches the symbol
msg=f.getMsg(isMfgDateCorr, isExpDateCorr, isDescCorr, isSymbCorr)# Get the final message (decision)
f.disp(msg, imgPath) # Display mssage on image
conn.close()
