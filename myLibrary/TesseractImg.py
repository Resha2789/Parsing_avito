from PIL import Image
import pytesseract
import os
import re


class TesseractImg:
    def __init__(self):
        pass

    def image_to_string(self):
        try:
            img = Image.open(os.path.abspath("Все для сборщика данных/Телефон.png"))
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
            custom_config = r'--oem 3 --psm 13 -c tessedit_char_whitelist=0123456789'
            text = pytesseract.image_to_string(img, config=custom_config)
            data = re.sub(r'\s+|[-]+', '', text)
            data = re.sub(r'[ОоOo]+', '0', data)
            data = int(re.sub(r'[^0-9]+', '', data))
            return data
        except Exception as error:
            print(f"image_to_string {error}")
            return 0


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    tes = TesseractImg()
    print(tes.image_to_string())
