# Получение карты рельфа местности
Данный способ работает только на Linux (Использовал Ubuntu 24.04).

Для получения карты рельефа местности в формате .tif по 2-ум координатам следует открыть терминал и ввести следущие команды:

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
То есть в терминале должна быть в начале строки надпись (venv).

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

Загрузка данных высот по координатам создаст файл .tif в текущей директории:
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
Для этого находясь в запущенном виртуальном окружении директории вашего проекта следует прописать в терминале следущее:
```bash
pip install elevation rasterio matplotlib
```

Создадим файл скрипта на python:
```bash
touch elevation.py
```

Открываем файл elevation.py через nano (или любой другой редактор):
```bash
nano elevation.py
```

Внутри файла прописываем следующий код:
```Python
import rasterio
import matplotlib.pyplot as plt

with rasterio.open('srtm.tif') as dataset:
    data = dataset.read(1)
    bounds = dataset.bounds
    extent = [bounds.left, bounds.right, bounds.bottom, bounds.top]

    plt.figure(figsize=(10, 8))
    plt.imshow(data, cmap='terrain', extent=extent, origin='upper')
    plt.colorbar(label='Высота (м)')
    plt.xlabel('Долгота')
    plt.ylabel('Широта')
    plt.title('Цифровая модель рельефа (SRTM)')
    plt.grid(True)

    # Сохранить карту в текущую директорию:
    plt.savefig('output_image.png', dpi=300)

    # Открыть карту в окне:
    plt.show(block=True)
```

Выход из файла elevation.py:

Ctrl + O (Сохранить?)

Enter (Подтвердить)

Cntrl + X (Закрыть)

Запуск скрипта elevation.py (карту высот можно сохранить):
```bash
python3 elevation.py
```

После этого откроется окно matplotlib с картой высот и она же появится в ваше директории в формате .png. Выглядит это так:
![height_map](https://github.com/user-attachments/assets/09fa007f-b2cb-4c26-ae3b-27c27d5c283f)



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

## Опционально можно удалить весь проект через терминал.
Удаление всего проекта со всем содержимым (выполняется из домашней директории):
```bash
rm -rf elevation_project
```

# Построение профиля рельефа местности.
Для построения профиля рельефа вам необходимо скачать содержимое репозитория и иметь файл карты высот в формате .tif (как его получить читайте выше).

Так же для этого потребуется ряд пакетов Python. Установить их можно прописав в терминале следущее:
```bash
pip install rasterio matplotlib numpy pyproj shapely
```
(Вроде бы это все? Непомню. Потом проверю как-нибудь.)

Файл .tiff следует положить в папку input.

Папка output служит для получения результатов.

Скрипт Elevation.py позволяет получть png картинку карты.

Скрипт Exports.py содержит функции экспорта, на которые ссылаются прочие скрипты.

Скрипт Relief_profile.py позволяет получить профиль рельефа. Выглядит это так:
![relief_profile](https://github.com/user-attachments/assets/a48d778b-ba23-4cc3-93a1-e60970ade311)

Также скрипт Relief_profile.py сгенерирует мини отчёт в формаде .mk в папку output. Выглядит это так:

[Отчет по профилю рельефа](output/relief_report.md)

Так же данные можно экспортировать в форматах .csv, .json.

Так же можно экспортировать интерактивную карту рельефа в .html формате.


