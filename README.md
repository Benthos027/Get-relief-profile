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

![height_map](https://github.com/user-attachments/assets/a07755f0-319c-497f-be4e-a01d8343697f)

### Скрипт Relief_profile_2_points.py
Скрипт Relief_profile.py позволяет получить профиль рельефа между двумя точками. Выглядит это так:

![relief_profile](https://github.com/user-attachments/assets/a48d778b-ba23-4cc3-93a1-e60970ade311)

Также скрипт Relief_profile_2_points.py сгенерирует мини отчёт в формате .md в папку output. Выглядит это так:

[Отчет по профилю рельефа](/samples/relief_report_2_points.md)

Так же данные можно экспортировать в форматах .csv, .json.

Так же можно экспортировать интерактивную карту рельефа в .html формате.

### Скрипт Relief_profile_multiple_points.py
Скрипт Relief_profile.py позволяет получить профиль рельефа на трассе построенной по множеству точек. Выглядит это так:

![relief_profile_multiple_points](/samples/relief_profile_multiple_points.png)

Также скрипт Relief_profile_multiple_points.py сгенерирует мини отчёт в формате .md в папку output. Выглядит это так:

[Отчет по профилю рельефа](/samples/relief_report_multiple_points.md)

Так же данные можно экспортировать в форматах .csv, .json.

Так же можно экспортировать интерактивную карту рельефа в .html формате.


