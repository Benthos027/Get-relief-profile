# Построение профиля рельефа местности.
Для построения профиля рельефа вам необходимо скачать содержимое репозитория и иметь файл карты высот в формате .tif, который можно получить по этой инструкции [Получение карты рельефа в формате .tif](/samples/instruction-1.md)

Так же для этого потребуется ряд пакетов Python. Установить их можно, прописав в терминале следующее:
```bash
pip install rasterio matplotlib numpy pyproj shapely elevation
```
(Вроде бы это все? Не помню. Потом проверю как-нибудь.)

Файл .tiff следует положить в папку input.

Папка output служит для получения результатов.

### Скрипт Exports.py
Скрипт Exports.py содержит функции экспорта, на которые ссылаются прочие скрипты.

### Скрипт Elevation.py
Скрипт Elevation.py позволяет получить png картинку карты высот. Выглядит это так:

![height_map](/samples/height_map.png)

### Скрипт Relief_profile_2_points.py
Скрипт Relief_profile.py позволяет получить профиль рельефа между двумя точками. Выглядит это так:

![Профиль по двум точкам](/samples/relief_profile_2_points.png)

Также скрипт Relief_profile_2_points.py сгенерирует мини отчёт в формате .md в папку output. Выглядит это так:

[Отчет по профилю рельефа из двух точек](/samples/relief_report_2_points.md)

Так же данные можно экспортировать в форматах .csv, .json.

Так же можно экспортировать интерактивную карту рельефа в .html формате. Выглядит это так:

![image](https://github.com/user-attachments/assets/1639601d-4281-45c9-a480-60a7d88ecbcb)


### Скрипт Relief_profile_multiple_points.py
Скрипт Relief_profile.py позволяет получить профиль рельефа на трассе построенной по множеству точек. Выглядит это так:

![Профиль по множеству точек](/samples/relief_profile_multiple_points.png)

Также скрипт Relief_profile_multiple_points.py сгенерирует мини отчёт в формате .md в папку output. Выглядит это так:

[Отчет по профилю рельефа из множества точек](/samples/relief_report_multiple_points.md)

Так же данные можно экспортировать в форматах .csv, .json.

Так же можно экспортировать интерактивную карту рельефа в .html формате. Выглядит это так:

![image](https://github.com/user-attachments/assets/3c51bc8f-0594-40ff-8c84-625fefdecf44)



