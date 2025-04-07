# Получение карты рельфа местности
Данный способ работает только на Linux (Использовал Ubuntu 24.04).
Для получения карты рельефа местности в формате .tiff по 2-ум координатам следует открыть терминал и ввести следущие команды:

Обновление пакетов:
sudo apt update
sudo apt upgrade (при необходимости)

Уснанавливаем виртуальное окружение venv и менеджер пакетов pip:
sudo apt install -y python3-pip python3-venv

Создание рабочей папки:
mkdir ~/elevation_project

Открытие рабочей папки в терминале:
cd ~/elevation_project

Создаем виртуальное окружение:
python3 -m venv venv

Активируем виртуальное окружение:
source venv/bin/activate

Дальше все делается внутри активного виртуального окружения!
То есть в терминале должна быть в начале строки надпись (.venv) 

Установка пакетов apt:
sudo apt install -y \
  gdal-bin \
  libgdal-dev \
  make \
  curl \
  python3-dev \
  build-essential \
  python3-tk

Установка пакетов pip:
pip install elevation rasterio matplotlib

Загрузка данных высот по координатам создаст файл srtm.tif в текущей директории:
eio clip -o {имя файла}.tif --bounds {Коордтнаты первой точки} {Координаты второй точки}

Например участок между НПС-1 и НПС-2 для своего диплома я получал так:
eio clip -o srtm.tif --bounds 134.8 48.8 135.3 49.6

Дальше создается файл скрипта на python:
touch elevation.py

Открываем файл elevation.py:
nano elevation.py

Внутри файла прописываем следующий код:

########## Начало файла elevation.py ##########

# Подключение библиотек:
import rasterio
import matplotlib.pyplot as plt

# Открываем GeoTIFF файл:
with rasterio.open('srtm.tif') as dataset:
    data = dataset.read(1)  # Первый канал (высоты)
    bounds = dataset.bounds  # Границы в координатах

    # bounds — это объект с четырьмя значениями: left, bottom, right, top
    extent = [bounds.left, bounds.right, bounds.bottom, bounds.top]

    # Визуализируем данные с координатной привязкой
    plt.figure(figsize=(10, 8))
    plt.imshow(data, cmap='terrain', extent=extent, origin='upper')
    plt.colorbar(label='Высота (м)')
    plt.xlabel('Долгота')
    plt.ylabel('Широта')
    plt.title('Цифровая модель рельефа (SRTM)')
    plt.grid(True)

    # Сохраняем изображение:
    # plt.savefig('output_image.png', dpi=300)

    # Показываем изображение
    plt.show(block=True)  # Эта строка блокирует завершение программы до закрытия окна

########## Конец файла elevation.py ##########

Выход из файла elevation.py:
Ctrl + O
Enter
Cntrl + X

Запуск скрипта elevation.py (карту высот можно сохранить):
python3 elevation.py

Выход из виртуального окружения:
deactivate  

Возвращаемся в домашнюю директорию:
cd ~

------------------------------------------------
Опционально можно открывать карту через qgis.
Установка qgis:
sudo apt install -y qgis

Запуск qgis:
qgis

Открыть .tiff файл можно так:
Ctrl + Shift + R, после указать путь до .tiff файла, нажать добавить, нажать закрыть.

------------------------------------------------
Опционально можно удалить все через терминал.
Удаление всего проекта со всем содержимым (выполняется из домашней директории):
rm -rf elevation_project



