# Получение карты рельфа местности
Данный способ работает только на Linux (Использовал Ubuntu 24.04).
Для получения карты рельефа местности в формате .tiff по 2-ум координатам следует открыть терминал и ввести следущие команды:

Обновление пакетов:
```bash
sudo apt update %% sudo apt upgrade
```

Уснанавливаем виртуальное окружение venv и менеджер пакетов pip:
```bash
sudo apt install -y python3-pip python3-venv
```

Создание рабочей папки:
```bash
mkdir ~/elevation_project
```

Открытие рабочей папки в терминале:
```bash
cd ~/elevation_project
```

Создаем виртуальное окружение:
```bash
python3 -m venv venv
```

Активируем виртуальное окружение:
```bash
source venv/bin/activate
```

Дальше все делается внутри активного виртуального окружения!
То есть в терминале должна быть в начале строки надпись (venv) 

Установка пакетов apt:
```bash
sudo apt install -y \
  gdal-bin \
  libgdal-dev \
  make \
  curl \
  python3-dev \
  build-essential \
  python3-tk
```

Установка пакетов pip:
```bash
pip install elevation
```

Загрузка данных высот по координатам создаст файл srtm.tif в текущей директории:
```bash
eio clip -o {имя файла}.tif --bounds {Коордтнаты первой точки} {Координаты второй точки}
```

Например участок между НПС-1 и НПС-2 для своего диплома я получал так:
```bash
eio clip -o srtm.tif --bounds 134.8 48.8 135.3 49.6
```
Готово! У вас в папке вашего проекта теперь лежит карта высот в формате .tif.

Выход из виртуального окружения:
```bash
deactivate
```

Вернуться в домашнюю директорию можно так:
```bash
cd ~
```

## Опционально карту можно открывать карту через matplotlib (библеотека для графиков и т.п. в Python) или преобразовав её в .png.
Для этого находясь в виртуальном окружении следует прописать в терминале следущее:
```bash
pip install elevation rasterio matplotlib
```

Создадим файл скрипта на python:
```bash
touch elevation.py
```

Открываем файл elevation.py через nano (или что либо еще на ваше усмотрение):
```bash
nano elevation.py
```

Внутри файла прописываем следующий код:
```Python
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
```

Выход из файла elevation.py:
Ctrl + O (Сохранить?)
Enter (Подтвердить)
Cntrl + X (Закрыть)

Запуск скрипта elevation.py (карту высот можно сохранить):
```bash
python3 elevation.py
```


## Опционально карту можно открывать карту через qgis.
Установка qgis:
```bash
sudo apt install -y qgis
```

Запуск qgis:
```bash
qgis
```

Открыть .tiff файл можно так:
Ctrl + Shift + R, после указать путь до .tiff файла, нажать добавить, нажать закрыть.

## Опционально можно удалить есь проект через терминал.
Удаление всего проекта со всем содержимым (выполняется из домашней директории):
```bash
rm -rf elevation_project
```



