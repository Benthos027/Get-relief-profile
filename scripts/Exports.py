import os
import csv
import json
import folium
import datetime
import matplotlib.pyplot as plt


def create_intput_directory():
    """ Проверка и создание папки 'intput', если она не существует """
    if not os.path.exists('../intput'):
        os.makedirs('../intput')


def create_output_directory():
    """ Проверка и создание папки 'output', если она не существует """
    if not os.path.exists('../output'):
        os.makedirs('../output')


def export_csv(heights_clean, distances_clean, slopes_percent):
    """ Экспорт в CSV """
    # Создаём папку output, если её нет:
    create_output_directory()

    csv_filename = "../output/relief_profile.csv"

    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Дистанция_км", "Высота_м", "Уклон_проценты"])

        for i in range(len(heights_clean)):
            distance = distances_clean[i]
            height = heights_clean[i]
            slope = slopes_percent[i] if i < len(slopes_percent) else ""  # последняя точка — без уклона
            writer.writerow([round(distance, 3), round(height, 2), round(slope, 2) if slope != "" else ""])


def export_json(heights_clean, distances_clean, slopes_percent):
    """ Экспорт в JSON """

    # Создаём папку output, если её нет:
    create_output_directory()

    json_data = []
    for i in range(len(heights_clean)):
        entry = {
            "distance_km": round(distances_clean[i], 3),
            "height_m": round(heights_clean[i], 2),
        }
        if i < len(slopes_percent):
            entry["slope_percent"] = round(slopes_percent[i], 2)
        json_data.append(entry)

    json_filename = "../output/relief_profile.json"
    with open(json_filename, 'w', encoding='utf-8') as file:
        json.dump(json_data, file, ensure_ascii=False, indent=2)


def export_markdown(coordinates,
                    distances, min_height, max_height,
                    max_slope_percent, line_of_sight_blocked,
                    min_clearance_value, min_clearance_distance, min_clearance_height,
                    report_filename="../output/relief_report.md",
                    plot_filename="../output/relief_profile.png"):
    """ Экспорт Markdown-отчёта """

    # Создаём папку output, если её нет:
    create_output_directory()

    # Сохраняем график:
    plt.savefig(plot_filename, dpi=300)

    # Формируем текст отчёта
    with open(report_filename, "w", encoding="utf-8") as report:
        report.write(f"# Отчёт по профилю рельефа\n")
        report.write(f"**Дата:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        for i, (lat, lon) in enumerate(coordinates):
            # report.write(f"**Точка {i}:** широта {lat}, долгота {lon}\n\n")
            report.write(f"**Начальная точка:** широта {lat}, долгота {lon}\n\n" if i == 0
                         else (f"**Конечная точка:** широта {lat}, долгота {lon}\n\n" if i == len(coordinates) - 1
                               else f"**Точка {i}:** широта {lat}, долгота {lon}\n\n"))
        report.write(f"## Основные характеристики рельефа:\n")
        report.write(f"- Общая длина: {round(distances[-1], 2)} км\n")
        report.write(f"- Мин. высота: {round(min_height, 2)} м\n")
        report.write(f"- Макс. высота: {round(max_height, 2)} м\n")
        report.write(f"- Перепад высот: {round(max_height - min_height, 2)} м\n")
        report.write(f"- Макс. уклон: {round(max_slope_percent, 2)} %\n\n")

        report.write(f"## Анализ прямой видимости:\n")
        if line_of_sight_blocked:
            report.write(f"- ❌ Прямая видимость нарушена.\n")
            report.write(f"- Мин. зазор: {round(min_clearance_value, 2)} м\n")
            report.write(f"- Расстояние до точки перекрытия: {round(min_clearance_distance, 2)} км\n")
            report.write(f"- Высота рельефа в этой точке: {round(min_clearance_height, 2)} м\n\n")
        else:
            report.write(f"- ✅ Прямая видимость не нарушена. Зазор >= 0 м на всём участке\n\n")

        report.write(f"## График профиля рельефа:\n")
        report.write(f"![Профиль рельефа]({plot_filename})\n")


def export_interactive_map(coordinates, path='../output/interactive_map.html'):
    """ Экспорт интерактивной карты с маршрутом по множеству координат """

    # Создаём папку output, если её нет:
    create_output_directory()

    # Вычисляем центр карты как среднее значение широты и долготы всех точек:
    avg_lat = sum(lat for lat, lon in coordinates) / len(coordinates)
    avg_lon = sum(lon for lat, lon in coordinates) / len(coordinates)

    # Создаем карту:
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=10)

    # Добавляем маршрут:
    folium.PolyLine(coordinates, color='blue', weight=2.5, opacity=1).add_to(m)

    # Добавляем маркеры: НПС-1, повороты, НПС-2
    folium.Marker(coordinates[0], popup="Начальная_точка", icon=folium.Icon(color='green')).add_to(m)
    folium.Marker(coordinates[-1], popup="Конечная_точка", icon=folium.Icon(color='red')).add_to(m)

    # При желании можно отметить промежуточные точки
    for i, coord in enumerate(coordinates[1:-1], start=1):
        folium.Marker(coord, popup=f"Точка_{i}", icon=folium.Icon(color='blue', icon='info-sign')).add_to(m)

    # Сохраняем карту:
    m.save(path)
