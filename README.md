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


