import pytesseract
from PIL import Image

image = Image.open(r"D:\anjiyou-api_automation_new\map.png")
image = image.convert("RGB")
text = pytesseract.image_to_string(image)
osd = pytesseract.image_to_osd(image)
print(text)