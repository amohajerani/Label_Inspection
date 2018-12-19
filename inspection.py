import datetime
from dateutil.relativedelta import relativedelta

import inspection_functions as f

# Update these paths where necessary
hourglass_symb = ''
BD_logo_symb = ''
db_path = ''

# Updat the catalog number information as necessary 
cat_first_3d = '515'
cat_len = 6

atr_lst = ['Mfg date', 'Expiry date', 'Product desc',
           'Product code', 'Hourglass', 'BD logo']

def inspect(img):
    # Inspect img and return:
    #[Date and time, img, Pass/Fail, Cause of Fail]
    # Print the results and log them to csv file.

    now = datetime.datetime.now()
    outpt = [str(now), img]

    # Check the symbols
    hourglass_pass = f.check_symb(img, hourglass_symb)
    BD_logo_pass = f.check_symb(img, BD_logo_symb)

    # Extract text from image
    txt = f.txt(img)
    
    if txt == '':
        outpt.append('Fail')
        outpt.append('Unreadable label')
        f.write_to_file(outpt)
        return

    try:
        cat_num_ind = txt.index(cat_first_3d)
        cat_num = ''.join(txt[cat_num_ind:cat_num_ind + cat_len])
    except:
        outpt.append('Fail')
        outpt.append('Missing Cat. No.')
        f.write_to_file(outpt)
        return    

    try:
        prod_atr = f.db(cat_num, db_path)
    except:
        outpt.append('Fail')
        outpt.append('Cat. number not found in database')
        f.write_to_file(outpt)
        return

    # Check mfg and expiry dates
    today_date = "%s-%s-%s" %(now.year, now.month, now.day)
    mfg_date_match = txt.find(today_date)!= -1

    exp_date = now+relativedelta(months=+prod_atr.shelf_life) 
    exp_date = "%s-%s-%s" %(exp_date.year, exp_date.month, exp_date.day)
    exp_date_match = txt.find(exp_date) != -1

    # Check product description and code
    desc_match = txt.find(prod_atr.descr) != -1
    code_match = txt.find(prod_atr.code) != -1


    # Create a list of mismatched attributes      
    atr_match = [mfg_date_match,
                 exp_date_match,
                 desc_match,
                 code_match,
                 hourglass_pass,
                 BD_logo_pass]

    
    if all(atr_match):
        outpt.append('Pass')
    else:
        outpt.append('Fail')
        fail_cause = str()
        for match, atr in zip(atr_match, atr_lst):
            if not match:inspection.py
               fail_cause = fail_cause + atr + ', '
    outpt.append(fail_cause)           
    f.write_to_file(outpt)
    return
    
# Run this script directly to inspect a single image.
# Enter the full image path, img_path
if __name__ == '__main__':
    img_path = ''
    inspect(img_path)
