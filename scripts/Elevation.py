import rasterio
import matplotlib.pyplot as plt

from Exports import create_output_directory

create_output_directory()  # Создаём папку output, если её нет

# Открываем GeoTIFF файл:
with rasterio.open('../input/srtm.tif') as dataset:
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
    plt.savefig('../output/height_map.png', dpi=300)

    # Показываем изображение
    plt.show(block=True)  # Эта строка блокирует завершение программы до закрытия окна
