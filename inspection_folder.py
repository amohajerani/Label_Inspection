# Inspect every image in img_dir

import os

import inspection

# Update this path if necessary
img_dir = ''

img_lst = [os.path.join(img_dir,f) for f in os.listdir(img_dir)]
img_lst = list(filter(os.path.isfile, img_lst))


for img in img_lst:  
    inspection.inspect(img)
