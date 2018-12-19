# Continously check the folder for new images.
# Perform inspection when a new imge is uploaded to the folder. 

import os

import inspection

# Update these paths if necessary   
img_dir = ""
db_path = ""

def img_newest(img_dir):
    # Return the path to the most recent image in the img_dir directory

    img_lst = [os.path.join(img_dir,f) for f in os.listdir(img_dir)]
    img_lst = list(filter(os.path.isfile, img_lst))
    img_lst.sort(key=os.path.getctime, reverse=True)
    cleanup(img_lst)
    img_newest = img_lst[0]
    return img_newest

def cleanup(img_lst, ct_max=100, ct_min=50):
    # Delete older images to free up memory.
    # Parameters:
    #   img_lst: Paths to all images in the directory
    #   ct_max, ct_min: min and max number of images allowed in directory

    if len(img_lst) > ct_max:
        for image in img_lst[ct_min:]:
            os.remove(image)

inspected=''

# Inspect newly uploaded images in img_dir directory.
while True:
    img = img_newest(img_dir)
    if img != inspected:
        inspection.inspect(img)
        inspected = img

