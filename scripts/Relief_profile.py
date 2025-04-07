import rasterio
import numpy as np
import matplotlib.pyplot as plt
from pyproj import Geod
from shapely.geometry import LineString
from Exports import export_csv, export_json, export_markdown, export_interactive_map

# Координаты начальной и конечной точки (широта, долгота):
point_1_lat, point_1_lon = 48.901265, 134.900967
point_2_lat, point_2_lon = 49.486001, 135.188316

# Путь к GeoTIFF (DEM в EPSG:4326)
geotiff_path = '../input/srtm.tif'

# Количество точек профиля:
num_samples = 500

# === Загрузка DEM ===

with rasterio.open(geotiff_path) as src:
    elevation_data = src.read(1)
    transform = src.transform
    crs = src.crs

# === Линия между точками в EPSG:4326 ===

line = LineString([(point_1_lon, point_1_lat), (point_2_lon, point_2_lat)])
sample_points = [line.interpolate(i / (num_samples - 1), normalized=True) for i in range(num_samples)]

# === Преобразование в координаты пикселя ===

pixel_coords = [~transform * (point.x, point.y) for point in sample_points]
rows_cols = [(int(r), int(c)) for c, r in pixel_coords]

# === Извлечение высот ===

profile_heights = []
for r, c in rows_cols:
    if 0 <= r < elevation_data.shape[0] and 0 <= c < elevation_data.shape[1]:
        profile_heights.append(elevation_data[r, c])
    else:
        profile_heights.append(np.nan)
profile_heights = np.array(profile_heights)


# === Сглаживание ===

def smooth_profile_reflect(profile, window_size=5):
    pad = window_size // 2
    padded = np.pad(profile, (pad, pad), mode='reflect')
    return np.convolve(padded, np.ones(window_size) / window_size, mode='valid')


smoothed_heights = smooth_profile_reflect(profile_heights, window_size=3)

# === Расчёт расстояний (в метрах) ===

geod = Geod(ellps="WGS84")
distances = [0.0]
for i in range(1, len(sample_points)):
    lon1, lat1 = sample_points[i - 1].x, sample_points[i - 1].y
    lon2, lat2 = sample_points[i].x, sample_points[i].y
    _, _, dist = geod.inv(lon1, lat1, lon2, lat2)
    distances.append(distances[-1] + dist)
distances = np.array(distances) / 1000  # в километрах

# === Прямая видимость ===

los_line = np.linspace(smoothed_heights[0], smoothed_heights[-1], len(smoothed_heights))
clearance = los_line - smoothed_heights
min_clearance_value = np.min(clearance)
min_clearance_index = np.argmin(clearance)
min_clearance_distance = distances[min_clearance_index]
min_clearance_height = smoothed_heights[min_clearance_index]
line_of_sight_blocked = np.any(clearance < 0)

# === Анализ уклонов ===

valid_mask = ~np.isnan(smoothed_heights)
heights_clean = smoothed_heights[valid_mask]
distances_clean = distances[valid_mask]

dy = np.diff(heights_clean)
dx = np.diff(distances_clean) * 1000  # в метрах
slopes = dy / dx
slopes_percent = slopes * 100
slopes_degrees = np.degrees(np.arctan(slopes))

max_slope_percent = np.max(np.abs(slopes_percent))
max_slope_deg = np.max(np.abs(slopes_degrees))

# === Вывод характеристик ===

print(f"🔹 Длина профиля: {distances[-1]:.2f} км")
print(f"🔹 Минимальная высота: {np.min(heights_clean):.1f} м")
print(f"🔹 Максимальная высота: {np.max(heights_clean):.1f} м")
print(f"🔹 Перепад высот: {np.max(heights_clean) - np.min(heights_clean):.1f} м")
print(f"🔹 Максимальный уклон: {max_slope_percent:.2f}% ({max_slope_deg:.2f}°)")
print(f"🔹 Прямая видимость {'ЗАБЛОКИРОВАНА' if line_of_sight_blocked else 'не заблокирована'}")
print(f"🔹 Мин. зазор: {min_clearance_value:.1f} м на {min_clearance_distance:.2f} км")

# === Построение графиков ===

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True, gridspec_kw={'height_ratios': [3, 1]})

# Профиль:
ax1.plot(distances, smoothed_heights, color='green', label='Сглаженный рельеф')
ax1.plot(distances, los_line, '--', color='purple', label='Прямая видимость')
ax1.plot(min_clearance_distance, min_clearance_height, 'ko', label='Мин. зазор')
ax1.set_xlabel("Расстояние (км)")

# Отметки НПС:
ax1.scatter(distances[0], smoothed_heights[0], color='blue', label='Точка 1')
ax1.scatter(distances[-1], smoothed_heights[-1], color='blue', label='Точка 2')
ax1.text(distances[0], smoothed_heights[0] + 35, "Точка 1", color='blue', fontsize=12, ha='left')
ax1.text(distances[-1], smoothed_heights[-1] + 35, "Точка 2", color='blue', fontsize=12, ha='right')

# Макс. уклон:
max_slope_idx = np.argmax(np.abs(slopes_percent))
max_slope_x = (distances_clean[max_slope_idx] + distances_clean[max_slope_idx + 1]) / 2
max_slope_y = (heights_clean[max_slope_idx] + heights_clean[max_slope_idx + 1]) / 2
ax1.plot(max_slope_x, max_slope_y, 'ro', label='Макс. уклон')

ax1.set_ylabel("Высота (м)")
ax1.set_title("Профиль рельефа между НПС")
ax1.legend()
ax1.tick_params(axis='x', labelbottom=True)  # включаем подписи
ax1.grid(True)

# Уклоны:
ax2.plot(distances_clean[:-1], slopes_percent, color='orange', label='Уклон (%)')
ax2.axvline(max_slope_x, color='red', linestyle='--', alpha=0.6, label='Макс. уклон')
ax2.set_xlabel("Расстояние (км)")
ax2.set_ylabel("Уклон (%)")
ax2.legend()
ax2.grid(True)

plt.tight_layout()

# === Экспорты ===

export_csv(heights_clean, distances_clean, slopes_percent)

export_json(heights_clean, distances_clean, slopes_percent)

export_markdown(point_1_lat, point_1_lon,
                point_2_lat, point_2_lon,
                distances,
                np.min(heights_clean),
                np.max(heights_clean),
                max_slope_percent,
                line_of_sight_blocked,
                min_clearance_value,
                min_clearance_distance,
                min_clearance_height)

export_interactive_map(point_1_lat, point_1_lon,
                       point_2_lat, point_2_lon)

# Отобразить график:
plt.show()
