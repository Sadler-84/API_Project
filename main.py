import pygame
import requests
import io
from urllib.parse import urlencode

LONGITUDE = 37.617635  # Начальная долгота (Москва)
LATITUDE = 55.755768  # Начальная широта (Москва)
ZOOM = 12  # Масштаб (1-17)
WINDOW_SIZE = (650, 450)
API_KEY = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"
DARK_MODE = False  # Переименовал переменную для ясности

MIN_LONGITUDE = -180
MAX_LONGITUDE = 180
MIN_LATITUDE = -85
MAX_LATITUDE = 85

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Яндекс.Карта")


def calculate_move_step(zoom):
    """Вычисляет шаг перемещения в зависимости от масштаба"""
    base_step = 0.1
    scale_factor = 2 ** (12 - zoom)
    step = base_step * scale_factor
    return max(0.0001, min(10.0, step))


def load_map(longitude, latitude, zoom, dark_mode=False):
    """Загружает карту из API Яндекс. Карт"""
    params = {
        'll': f"{longitude},{latitude}",
        'z': zoom,
        'size': f"{WINDOW_SIZE[0]},{WINDOW_SIZE[1]}",
        'l': 'map',  # Основной слой
        'apikey': API_KEY
    }

    #Добавляем темную тему
    if dark_mode:
        params['theme'] = 'dark'

    url = f"https://static-maps.yandex.ru/1.x/?{urlencode(params)}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        image_bytes = io.BytesIO(response.content)
        return pygame.image.load(image_bytes)
    except Exception as e:
        print(f"Ошибка загрузки карты: {e}")
        error_surface = pygame.Surface(WINDOW_SIZE)
        error_surface.fill((150, 150, 150))
        return error_surface


def adjust_coordinates(lon, lat):
    """Корректирует координаты в допустимых пределах"""
    lon = max(MIN_LONGITUDE, min(MAX_LONGITUDE, lon))
    lat = max(MIN_LATITUDE, min(MAX_LATITUDE, lat))
    return lon, lat


current_lon, current_lat = LONGITUDE, LATITUDE
map_image = load_map(current_lon, current_lat, ZOOM, DARK_MODE)

running = True
clock = pygame.time.Clock()
while running:
    move_step = calculate_move_step(ZOOM)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Изменение масштаба
            if event.key == pygame.K_PAGEUP and ZOOM < 17:
                ZOOM += 1
                map_image = load_map(current_lon, current_lat, ZOOM, DARK_MODE)
            elif event.key == pygame.K_PAGEDOWN and ZOOM > 1:
                ZOOM -= 1
                map_image = load_map(current_lon, current_lat, ZOOM, DARK_MODE)
            # Перемещение карты
            elif event.key == pygame.K_UP:
                current_lat += move_step
                current_lon, current_lat = adjust_coordinates(current_lon, current_lat)
                map_image = load_map(current_lon, current_lat, ZOOM, DARK_MODE)
            elif event.key == pygame.K_DOWN:
                current_lat -= move_step
                current_lon, current_lat = adjust_coordinates(current_lon, current_lat)
                map_image = load_map(current_lon, current_lat, ZOOM, DARK_MODE)
            elif event.key == pygame.K_LEFT:
                current_lon -= move_step
                current_lon, current_lat = adjust_coordinates(current_lon, current_lat)
                map_image = load_map(current_lon, current_lat, ZOOM, DARK_MODE)
            elif event.key == pygame.K_RIGHT:
                current_lon += move_step
                current_lon, current_lat = adjust_coordinates(current_lon, current_lat)
                map_image = load_map(current_lon, current_lat, ZOOM, DARK_MODE)
            # Перключение в темную тему
            elif event.key == pygame.K_d:
                DARK_MODE = not DARK_MODE
                map_image = load_map(current_lon, current_lat, ZOOM, DARK_MODE)

    # Отрисовка
    screen.blit(map_image, (0, 0))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()