from pyproj import Transformer
import rasterio
from shapely.geometry import LineString

geotiff_path = '../input/srtm.tif'

# Координаты двух точек (широта, долгота)
point_1_lat, point_1_lon = 48.901265, 134.900967  # Точка 1
point_2_lat, point_2_lon = 49.486001, 135.188316  # Точка 2

# Кол-во точек профиля
num_samples = 500

with rasterio.open(geotiff_path) as src:
    elevation_data = src.read(1)  # Читаем только первый канал
    transform = src.transform  # Affine-преобразование
    crs = src.crs  # Система координат файла

with rasterio.open(geotiff_path) as dataset:
    print(dataset.meta)

# Переводим в UTM зона 52N — EPSG:32652
transformer = Transformer.from_crs(crs, "EPSG:32652", always_xy=True)

nps1_x, nps1_y = transformer.transform(point_1_lon, point_1_lat)
nps2_x, nps2_y = transformer.transform(point_2_lon, point_2_lat)

line = LineString([(nps1_x, nps1_y), (nps2_x, nps2_y)])  # теперь в метрах

print(f"Длина профиля (метров): {line.length}")
