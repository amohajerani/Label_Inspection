Read this before running the code:
-	Make sure the paths to images and database are put correctly in inspection.py, inspect_folder.py,  and main.py.
-	Run main.py if you are interested in continuously monitoring and image directory and inspecting new uploads (e.g. in production setting).
-	Run inspect_folder.py if you are interested in inspecting all images in the directory.
-	Run insection.py if you are interested in inspecting single image.
Background
- This is a pet project, not an official project.
- The code can inspect text and symbols on the labels.
- The code is not intended to read barcodes. 

Structure of the code

main.py
 Constantly monitor image directory and when there is a new image, call the inspection module to inspect the image.
 Free up space periodically by deleting old images.

Inspection.py
The inspect function accepts the image and returns the inspection results (pass/fail) along with cause(s) of the fail.
The function inspects text and symbols. Inspection is done in three parts: text inspection, symbol inspection, and reporting the output.

Part 1: Text inspection
Step 1: Open, binarize and filter image, using OpenCV library.
Step 2: Extract text from the image using Tesseract library.
Step 3: Compare this text to the information in product database, and check the validity of
-	Catalog #
-	Manufacturing date
-	Expiry date
-	Product description
-	Product code
Part 2: Symbol inspection
Template matching was performed to identify symbols.
Step 1: Open, binarize and filter image and template, using OpenCV library.
Step 2: Perform template matching. The output is a ndarray of r values.
Step 3: Pass the symbol inspection if maximum r value > threshold.

Part 3
Print the summary of inspection results and write it to a csv file.


