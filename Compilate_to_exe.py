import PyInstaller.__main__
import shutil
import os
import sys

def install(sistem=64):
    folder = 'Parsing_uslugio_ru_64bit'
    if sistem == 32:
        folder = 'Parsing_uslugio_ru_62bit'

    src_data = f"D:\Programming\Python\{folder}\Все для сборщика данных"
    dst_data = f"D:\Фриланс\Авито\{folder}\Все для сборщика данных"
    try:
        shutil.rmtree(dst_data)
    except FileNotFoundError:
        print('Файл не найден!')

    shutil.copytree(src_data, dst_data, ignore=shutil.ignore_patterns('*.pyc', 'tmp*'))

    PyInstaller.__main__.run([
        "Main.py",
        "--noconsole",
        "--onefile",
        f"--icon=D:/Programming/Python/{folder}/""Все для сборщика данных/icon_phone.ico",
        f"--distpath=D:/Фриланс/Авито/{folder}/",
        "-n=Сборщик_телефонов_64bit"
    ])

if __name__ == '__main__':
    install(sistem=64)
