from selenium.webdriver.common.by import By
from selenium import webdriver
from myLibrary import MainWindow, DriverChrome, TesseractImg
from myLibrary.UslugioLibrary import ParsingThreading
import time


class ParsingUslugio(DriverChrome.Execute, TesseractImg.TesseractImg):
    def __init__(self, mainWindow=None, uslugioThreading=None, *args, **kwargs):
        super(ParsingUslugio, self).__init__(mainWindow=mainWindow, *args, **kwargs)
        self.mainWindow = mainWindow
        self.uslugioThreading = uslugioThreading
        self.stop_parsing = False
        self.pause_parsing = False
        self.urls_in_page = None
        self.services_in_page = None
        self.current_page = 1
        self.last_page = None
        self.total_found = 0

    def start_parsing_avito(self):
        m: MainWindow.MainWindow
        m = self.mainWindow

        u: ParsingThreading.UslugioThreading
        u = self.uslugioThreading

        self.driver: webdriver.Firefox
        time.sleep(10)

        # Всего найдено
        total = self.execute_js(rt=True, t=2, exit_loop=True, data='count_all_items()')
        print(f"$<b style='color: rgb(255, 196, 17);'>По ключевому слову {u.key_word} найдено: {total}</b>")

        try:
            while True:

                # Завершаем если парсинг остановлен
                if not m.parsing_avito:
                    return

                # Последняя страница
                self.last_page = self.execute_js(rt=True, t=2, exit_loop=True, data='last_page()')
                print(f'Последняя страница {self.last_page}')

                print('Все заголовки и url предлогаемых услуг')
                # Все заголовки и url предлогаемых услуг
                result = self.execute_js(rt=True, t=2, exit_loop=True, data='get_title_and_url_items()')
                self.services_in_page = result[0]
                self.urls_in_page = result[1]

                print(f"На странице найдено: {len(self.urls_in_page)}")

                # Количество предлогаемых услуг на странице
                total_in_page = len(self.services_in_page)

                for i in range(0, total_in_page):
                    # Количество попыток
                    for retry in range(0, 5):
                        if retry >= 4:
                            self.up_date()

                        # Завершаем если парсинг остановлен
                        if not m.parsing_avito:
                            return

                        # Рандомное приостановка выполнения
                        # time.sleep(random.randrange(5, 7))

                        if self.services_in_page[i] not in m.out_service:

                            print('Открываем url клиента')
                            # Открываем url клиента
                            self.driver.get(self.urls_in_page[i])

                            time.sleep(2)

                            print('Устанавливаем на страницу скрипты')
                            # Устанавливаем на страницу скрипты
                            if not self.set_library():
                                print('back continue')
                                continue

                            print('Контактное лицо')
                            # Контактное лицо
                            name = self.execute_js(sl=2, rt=True, t=2, exit_loop=True, data=f"name()")
                            if not name:
                                print('back continue')
                                continue

                            print('Показываем номер телефона')
                            # Показываем номер телефона
                            result = self.execute_js(sl=2, rt=True, t=2, exit_loop=True, data=f"click_phone()")
                            if not result:
                                print('back continue')
                                continue
                            if result == "Без звонков":
                                print("БEЗ ЗВОНКОВ")
                                break

                            print('Устанавливем элементу свой id')
                            # Устанавливем элементу свой id
                            result = self.execute_js(sl=2, rt=True, t=2, exit_loop=True, data=f"set_id_for_phone()")
                            if not result:
                                print('back continue')
                                continue

                            time.sleep(2)

                            print("Сохранаяем картинку номера телефона")
                            # Сохранаяем картинку номера телефона
                            with open('Все для сборщика данных/Телефон.png', 'wb') as file:
                                file.write(self.driver
                                           .find_element(By.XPATH, '//img[@id="phone_number"]')
                                           .screenshot_as_png)

                            # Распознаем цифры с картинки
                            phone_number = self.image_to_string()
                            if type(phone_number) == bool:
                                m.parsing_avito = False
                                return False

                            # Телефоны
                            m.out_phone_number.append(phone_number)

                            # Имена
                            m.out_full_name.append(name)

                            # Услуги
                            m.out_service.append(self.services_in_page[i])

                            # Города
                            m.out_city.append(m.inp_city)

                            # Ключевое слово
                            m.out_key_word.append(u.key_word)

                            # url клиента
                            m.out_url.append(self.urls_in_page[i])

                            # Массив данных для записи в Excel
                            m.out_avito_all_data.append(
                                [m.out_full_name[-1],
                                 m.out_service[-1],
                                 m.out_phone_number[-1],
                                 m.out_key_word[-1],
                                 m.out_city[-1],
                                 m.out_url[-1]])

                            print(f"$<b style='color: rgb(0, 203, 30);'>"
                                  f"{len(m.out_service)}. "
                                  f"{m.out_full_name[-1]}, "
                                  f"{m.out_service[-1]}, "
                                  f"{phone_number}, "
                                  f"{m.out_key_word[-1]}"
                                  f"</b>")
                            # Посылаем сигнал на главное окно в прогресс бар uslugio
                            m.Commun.progressBar.emit({'i': self.total_found + i, 'items': total})
                            # Активируем кнопку остановки
                            if not m.webdriver_loaded:
                                m.Commun.pushButton_uslugio_stop_enabled.emit(True)

                            break
                        break

                if self.current_page == self.last_page:
                    # Посылаем сигнал на главное окно в прогресс бар uslugio
                    m.Commun.progressBar.emit({'i': (self.total_found + total_in_page) - 1, 'items': total})
                    self.current_page = 1
                    self.total_found = 0
                    return
                else:
                    # Активируем кнопку остановки
                    if not m.webdriver_loaded:
                        m.Commun.pushButton_uslugio_stop_enabled.emit(True)

                    self.main_page()

                    self.current_page += 1
                    print(f"$<b style='color: rgb(16, 28, 255);'>Переход на следующию страницу {self.current_page}</b>")
                    result = self.execute_js(rt=True, t=2, exit_loop=True, data=f"next_page({self.current_page})")
                    if not result:
                        self.up_date()
                    time.sleep(15)

                    print('Устанавливаем на страницу скрипты')
                    # Устанавливаем на страницу скрипты
                    if not self.set_library():
                        self.up_date()

                    self.total_found += total_in_page
                    # Посылаем сигнал на главное окно в прогресс бар uslugio
                    m.Commun.progressBar.emit({'i': self.total_found, 'items': total})


        except Exception as detail:
            print("ERROR start_parsing_avito", detail)
            self.up_date()

    def main_page(self):
        u: ParsingThreading.UslugioThreading
        u = self.uslugioThreading

        # Проверка находимся ли мы на главной странице
        total = self.execute_js(rt=True, t=2, exit_loop=True, data='count_all_items()')
        if type(total) == bool:
            print(f"Переход на главную страницу")
            self.driver.get(u.url)
            time.sleep(10)
            print('Устанавливаем на страницу скрипты')
            # Устанавливаем на страницу скрипты
            if not self.set_library():
                time.sleep(5)
                return self.main_page()

    def up_date(self):
        try:
            m: MainWindow.MainWindow
            m = self.mainWindow

            u: ParsingThreading.UslugioThreading
            u = self.uslugioThreading

            print('UP_DATE')

            if not m.parsing_avito:
                return

            # Запус WebDriver
            if not self.star_driver(url=u.url):
                return
            # Устанавливаем на вебсайт скрипты
            if not self.set_library():
                return

            # Запускаем цикл парсинга uslugio
            self.start_parsing_avito()

        except Exception as detail:
            print("ERROR up_date:", detail)
            time.sleep(10)
            return
