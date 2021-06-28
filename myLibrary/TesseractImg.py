from PIL import Image
import pytesseract
import os
import re
import winapps


class TesseractImg:
    def __init__(self):
        self.path_tesseract = None

    def image_to_string(self):
        try:
            if not self.find_tesseract():
                return False
            img = Image.open(os.path.abspath("Все для сборщика данных/Телефон.png"))
            # r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
            pytesseract.pytesseract.tesseract_cmd = self.path_tesseract
            custom_config = r'--oem 3 --psm 23 -c tessedit_char_whitelist=0123456789'
            text = pytesseract.image_to_string(img, config=custom_config)
            data = re.sub(r'\s+|[-]+', '', text)
            data = re.sub(r'[ОоOo]+', '0', data)
            data = int(re.sub(r'[^0-9]+', '', data))
            return data
        except Exception as error:
            print(f"image_to_string {error}")
            return 0

    def find_tesseract(self):
        try:
            for app in winapps.search_installed('Tesseract-OCR'):
                test = app.uninstall_string
                self.path_tesseract = re.sub(r'uninstall.exe', 'tesseract.exe', r"" + str(app.uninstall_string))
                print(self.path_tesseract)
        except Exception as error:
            pass

        if self.path_tesseract is None:
            print(f"$<b style='color: rgb(255, 0, 0);'>Tesseract не найден! Установите Tesseract!</b>")
            return False

        return True
