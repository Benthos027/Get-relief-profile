import rasterio
import numpy as np
import matplotlib.pyplot as plt
from pyproj import Geod, Transformer
from shapely.geometry import LineString, Point
from scipy.ndimage import gaussian_filter1d
from Exports import export_csv, export_json, export_markdown, export_interactive_map

# Входные данные:
coordinates = [
    (48.90445, 134.89769),  # НПС-1
    (48.91026, 134.89048),  # ответвление к НПС-1
    (48.96427, 134.93829),  # Поворот 1
    (49.01108, 135.00463),  # Поворот 2
    (49.05109, 135.10763),  # Поворот 3
    (49.13736, 135.15561),  # Поворот 4
    (49.20930, 135.07725),  # Поворот 5
    (49.26596, 135.10351),  # Поворот 6
    (49.37500, 135.16737),  # Поворот 7
    (49.44910, 135.23569),  # ответвление к НПС-2
    (49.48491, 135.19003)  # НПС-2
]

# Путь к GeoTIFF (DEM в EPSG:4326)
geotiff_path = '../input/srtm.tif'

# Настройки
num_samples = 1000
smooth_coefficient = 9
smooth_type = 1    # 0 - без сглаживания, 1 - зеркальное, 3 - Гауссовский фильтр

# Включение экспорта:
export_to_csv = False
export_to_json = False
export_to_markdown = False
export_to_interactive_map = False

# Загрузка DEM:
with rasterio.open(geotiff_path) as src:
    elevation_data = src.read(1)
    transform = src.transform
    crs = src.crs

# Преобразование координат в проекцию UTM (пример — зона 52N):
transformer_to_utm = Transformer.from_crs("EPSG:4326", "EPSG:32652", always_xy=True)
transformer_to_wgs = Transformer.from_crs("EPSG:32652", "EPSG:4326", always_xy=True)

# Преобразованные точки в метрах (x, y):
utm_coords = [transformer_to_utm.transform(lon, lat) for lat, lon in coordinates]
utm_line = LineString(utm_coords)

# Дискретизация линии в UTM:
sample_points_utm = [utm_line.interpolate(i / (num_samples - 1), normalized=True) for i in range(num_samples)]

# Перевод точек обратно в широту/долготу для доступа к DEM:
sample_points_wgs = [Point(*transformer_to_wgs.transform(pt.x, pt.y)) for pt in sample_points_utm]

# Преобразование точек в пиксельные координаты:
pixel_coords = [~transform * (point.x, point.y) for point in sample_points_wgs]
rows_cols = [(int(r), int(c)) for c, r in pixel_coords]

# Извлечение высот:
profile_heights = []
for r, c in rows_cols:
    if 0 <= r < elevation_data.shape[0] and 0 <= c < elevation_data.shape[1]:
        profile_heights.append(elevation_data[r, c])
    else:
        profile_heights.append(np.nan)
profile_heights = np.array(profile_heights)


def smooth_profile_reflect(profile, window_size=5):
    """Функция зеркального сглаживания"""
    pad = window_size // 2
    padded = np.pad(profile, (pad, pad), mode='reflect')
    return np.convolve(padded, np.ones(window_size) / window_size, mode='valid')


# Сглаживание:
if smooth_type == 1:
    smoothed_heights = smooth_profile_reflect(profile_heights, window_size=smooth_coefficient)
elif smooth_type == 2:
    smoothed_heights = gaussian_filter1d(profile_heights, sigma=1)
else:
    smoothed_heights = profile_heights

# Расчёт расстояний:
geod = Geod(ellps="WGS84")
distances = [0.0]
for i in range(1, len(sample_points_wgs)):
    lon1, lat1 = sample_points_wgs[i - 1].x, sample_points_wgs[i - 1].y
    lon2, lat2 = sample_points_wgs[i].x, sample_points_wgs[i].y
    _, _, dist = geod.inv(lon1, lat1, lon2, lat2)
    distances.append(distances[-1] + dist)
distances = np.array(distances) / 1000  # км

# Анализ уклонов:
valid_mask = ~np.isnan(smoothed_heights)
heights_clean = smoothed_heights[valid_mask]
distances_clean = distances[valid_mask]

slopes = np.diff(heights_clean) / (np.diff(distances_clean) * 1000)  # м/м
slopes_percent = slopes * 100
slopes_degrees = np.degrees(np.arctan(slopes))

max_slope_percent = np.max(np.abs(slopes_percent))
max_slope_deg = np.max(np.abs(slopes_degrees))

# Прямая видимость:
los_line = np.linspace(heights_clean[0], heights_clean[-1], len(heights_clean))
clearance = los_line - heights_clean
min_clearance_value = np.min(clearance)
min_clearance_index = np.argmin(clearance)
min_clearance_distance = distances_clean[min_clearance_index]
min_clearance_height = heights_clean[min_clearance_index]
line_of_sight_blocked = np.any(clearance < 0)

# ывод характеристик:
print(f"🔹 Длина профиля: {distances[-1]:.2f} км")
print(f"🔹 Минимальная высота: {np.min(heights_clean):.1f} м")
print(f"🔹 Максимальная высота: {np.max(heights_clean):.1f} м")
print(f"🔹 Перепад высот: {np.max(heights_clean) - np.min(heights_clean):.1f} м")
print(f"🔹 Максимальный уклон: {max_slope_percent:.2f}% ({max_slope_deg:.2f}°)")
print(f"🔹 Прямая видимость {'ЗАБЛОКИРОВАНА' if line_of_sight_blocked else 'не заблокирована'}")
print(f"🔹 Мин. зазор: {min_clearance_value:.1f} м на {min_clearance_distance:.2f} км")

# Построение графиков:
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True, gridspec_kw={'height_ratios': [3, 1]})

ax1.plot(distances_clean, heights_clean, label='Рельеф', color='green')
ax1.plot(distances_clean, los_line, '--', label='Прямая видимость', color='purple')
ax1.plot(min_clearance_distance, min_clearance_height, 'ko', label='Мин. зазор')

# Подписи ключевых точек:
for i, (lat, lon) in enumerate(coordinates):
    point = Point(*transformer_to_utm.transform(lon, lat))
    distance_along = utm_line.project(point) / utm_line.length * distances_clean[-1]
    idx = np.argmin(np.abs(distances_clean - distance_along))
    height = heights_clean[idx]

    label = "Начальная точка" if i == 0 else (
        "Конечная точка" if i == len(coordinates) - 1 else f"Точка {i}\n({lat:.3f}, {lon:.3f})")
    color = 'purple' if i in (0, len(coordinates) - 1) else 'blue'

    ax1.scatter(distance_along, height, s=30, color=color, zorder=5)
    ax1.text(distance_along, height + 5, label, fontsize=8, ha='center', color=color,
             bbox=dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.1', alpha=0.5))

# Макс. уклон:
max_slope_idx = np.argmax(np.abs(slopes_percent))
max_slope_x = (distances_clean[max_slope_idx] + distances_clean[max_slope_idx + 1]) / 2
max_slope_y = (heights_clean[max_slope_idx] + heights_clean[max_slope_idx + 1]) / 2
ax1.plot(max_slope_x, max_slope_y, 'ro', label='Макс. уклон')

ax1.set_ylabel("Высота (м)")
ax1.set_title("Профиль рельефа")
ax1.grid(True)
ax1.legend()

# Уклоны:
ax2.plot(distances_clean[1:], slopes_percent, label='Уклон (%)', color='orange')
ax2.axvline(max_slope_x, linestyle='--', color='red', label='Макс. уклон')
ax2.set_xlabel("Расстояние (км)")
ax2.set_ylabel("Уклон (%)")
ax2.grid(True)
ax2.legend()

plt.tight_layout()

# Экспорты:
if export_to_csv:
    export_csv(heights_clean, distances_clean, slopes_percent)
if export_to_json:
    export_json(heights_clean, distances_clean, slopes_percent)
if export_to_markdown:
    export_markdown(coordinates,
                    distances,
                    np.min(heights_clean),
                    np.max(heights_clean),
                    max_slope_percent,
                    line_of_sight_blocked,
                    min_clearance_value,
                    min_clearance_distance,
                    min_clearance_height,
                    report_filename="../output/relief_report_multiple_points.md",
                    plot_filename="../output/relief_profile_multiple_points.png")
if export_to_interactive_map:
    export_interactive_map(coordinates, path='../output/interactive_map_multiple_points.html')

# Показать графики:
plt.show()
