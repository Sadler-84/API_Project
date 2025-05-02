import pygame
import requests
import io
from urllib.parse import urlencode

# Настройки карты
LONGITUDE = 37.617635  # Долгота (Москва)
LATITUDE = 55.755768  # Широта (Москва)
ZOOM = 12  # Масштаб (1-17)
WINDOW_SIZE = (650, 450)
API_KEY = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"


pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Яндекс.Карта")


def load_map(longitude, latitude, zoom):
    """Загружает карту из API Яндекс. Карт без сохранения в файл"""
    params = {
        'll': f"{longitude},{latitude}",
        'z': zoom,
        'size': f"{WINDOW_SIZE[0]},{WINDOW_SIZE[1]}",
        'l': 'map',
        'apikey': API_KEY
    }

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


map_image = load_map(LONGITUDE, LATITUDE, ZOOM)

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(map_image, (0, 0))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()