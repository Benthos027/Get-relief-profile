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


def export_markdown(point_1_lat, point_1_lon, point_2_lat, point_2_lon,
                    distances, min_height, max_height,
                    max_slope_percent, line_of_sight_blocked,
                    min_clearance_value, min_clearance_distance, min_clearance_height):
    """ Экспорт Markdown-отчёта """

    # Создаём папку output, если её нет:
    create_output_directory()

    # Путь и имя куда сохранять:
    report_filename = "../output/relief_report.md"
    plot_filename = "../output/relief_profile.png"

    # Сохраняем график:
    plt.savefig(plot_filename, dpi=300)

    # Формируем текст отчёта
    with open(report_filename, "w", encoding="utf-8") as report:
        report.write(f"# Отчёт по профилю рельефа\n")
        report.write(f"**Дата:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        report.write(f"**Начальная точка:** широта {point_1_lat}, долгота {point_1_lon}\n\n")
        report.write(f"**Конечная точка:** широта {point_2_lat}, долгота {point_2_lon}\n\n")

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


def export_interactive_map(point_1_lat, point_1_lon, point_2_lat, point_2_lon):
    """ Экспорт интерактивной карты """

    # Создаём папку output, если её нет:
    create_output_directory()

    # Создаем карту с фоновым слоем:
    m = folium.Map(location=[(point_1_lat + point_2_lat) / 2, (point_1_lon + point_2_lon) / 2], zoom_start=10)

    # Добавляем маршрут на карту:
    folium.PolyLine([(point_1_lat, point_1_lon), (point_2_lat, point_2_lon)], color='blue', weight=2.5,
                    opacity=1).add_to(m)

    # Добавляем маркеры НПС:
    folium.Marker([point_1_lat, point_1_lon], popup="НПС-1", icon=folium.Icon(color='green')).add_to(m)
    folium.Marker([point_2_lat, point_2_lon], popup="НПС-2", icon=folium.Icon(color='red')).add_to(m)

    # Сохраняем карту в файл:
    m.save('../output/profile_map.html')
