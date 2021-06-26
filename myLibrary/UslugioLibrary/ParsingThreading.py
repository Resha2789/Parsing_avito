import time

from myLibrary.UslugioLibrary.ParsingLib import ParsingUslugio
from PyQt5.QtCore import QThread
from myLibrary import MainWindow, Slug
import threading


class UslugioThreading(QThread, ParsingUslugio, Slug.Slugify):
    def __init__(self, mainWindow=None, *args, **kwargs):
        self.url = ''
        self.mainWindow = mainWindow
        self.key_word = ''
        self.working = False
        super(UslugioThreading, self).__init__(mainWindow=mainWindow, uslugioThreading=self, *args, **kwargs)

    def run(self):
        m: MainWindow.MainWindow
        m = self.mainWindow

        self.working = True

        threading.Thread(target=self.tim_out_thread).start()

        for i in m.inp_key_words:
            if self.stop_parsing or not m.parsing_avito:
                break

            # Посылаем сигнал на главное окно в textBrowser_uslugio_key_words
            m.Commun.uslugio_change_key_words.emit(i)

            self.key_word = i
            self.url = f"https://www.avito.ru/{self.slugify(m.inp_city)}/predlozheniya_uslug?q={i}"

            # Запус WebDriverChrome
            if not self.star_driver(url=self.url, proxy=False):
                return

            # Устанавливаем на вебсайт скрипты
            if not self.set_library():
                return

            # Запускаем цикл парсинга uslugio
            self.start_parsing_avito()

            # Посылаем сигнал на главное окно в прогресс бар avito
            m.Commun.uslugio_progressBar.emit({'i': 0, 'items': 100})

        if m.parsing_avito:
            m.avito_stop_threading()

        self.working = False

    def stop_threading(self):
        m: MainWindow.MainWindow
        m = self.mainWindow

        m.log = False
        m.parsing_avito = False
        save = False
        total = 0

        while True:
            if not self.working:
                # Запись в EXcel
                if m.write_to_excel():
                    save = True
                else:
                    save = False

                if self.driver is not None:
                    self.driver.quit()

                print("Программа завершена")

                self.kill_geckodriver()
                break

            total += 10
            # Посылаем сигнал на главное окно в прогресс бар uslugio
            m.Commun.uslugio_progressBar.emit({'i': total, 'items': 100})
            time.sleep(2)
            print(f"$Ждите, идет процесс завершения программы.")


        m.log = True

        print(f"$Сбор данных закончили\n$Всего собрано: {len(m.out_avito_all_data)}")
        if save:
            print(f"$Данные сохранились успешно {m.inp_name_excel_avito}")
        else:
            print(f"$Данные не сохранились!")

        # Посылаем сигнал на главное окно в прогресс бар uslugio
        m.Commun.uslugio_progressBar.emit({'i': 99, 'items': 100})
        m.pushButton_uslugio_start.setEnabled(True)
        m.uslugio_threading = None
