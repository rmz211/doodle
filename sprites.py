import pygame
import random
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/images/player_idle.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (PLAYER_START_X, PLAYER_START_Y)
        self.vel_y = 0
        self.move_speed = PLAYER_SPEED
        self.direction_x = 0

    def update(self):
        # обновление позиции игрока
        self.rect.x += self.direction_x * self.move_speed
        self.rect.y += self.vel_y
        self.vel_y += GRAVITY

        # границы экрана
        if self.rect.left < 0:
            self.rect.right = SCREEN_WIDTH
        if self.rect.right > SCREEN_WIDTH:
            self.rect.left = 0

    def jump(self):
        self.vel_y = -JUMP_STRENGTH  # обновляем прыжок

    def move_left(self):
        self.direction_x = -1

    def move_right(self):
        self.direction_x = 1

    def stop(self):
        self.direction_x = 0


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, platform_type="static"):
        super().__init__()
        self.type = platform_type

        # выбор изображения платформы
        platform_images = {
            "static": "assets/images/platform_static.png",
            "breaking": "assets/images/platform_breaking.png",
            "disappearing": "assets/images/platform_disappearing.png",
            "broken": "assets/images/platform_broken.png",
        }
        self.image = pygame.image.load(platform_images[platform_type]).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, PLATFORM_HEIGHT))
        self.rect = self.image.get_rect(topleft=(x, y))

        # скорость и направление платформы
        self.speed_x = random.randint(PLATFORM_SPEED_MIN, PLATFORM_SPEED_MAX) if self.type != "static" else 0
        self.speed_y = random.randint(PLATFORM_SPEED_MIN, PLATFORM_SPEED_MAX) if self.type != "static" else 0

        if self.type != "static":
            self.speed_x *= random.choice([-1, 1])
            self.speed_y *= random.choice([-1, 1])

    def update(self):
        # обновление позиции для движущихся платформ
        if self.type != "static":
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y

            # границы движения
            if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
                self.speed_x = -self.speed_x
            if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
                self.speed_y = -self.speed_y

    @staticmethod
    def generate_new():
        x = random.randint(0, SCREEN_WIDTH - PLATFORM_WIDTH_MIN)
        y = random.randint(-100, -10)
        width = random.randint(PLATFORM_WIDTH_MIN, PLATFORM_WIDTH_MAX)
        platform_type = random.choice(["static", "breaking", "disappearing", "broken"])
        return Platform(x, y, width, platform_type)


def create_sprite_groups(level):
    player_group = pygame.sprite.GroupSingle(Player())
    platform_group = pygame.sprite.Group()

    # создание стартовую платформу под игроком
    start_platform = Platform(PLAYER_START_X - 50, PLAYER_START_Y + 50, 120, "static")
    platform_group.add(start_platform)

    # создание остальных платформ
    num_platforms = {"easy": 9, "medium": 7, "hard": 6}[level]
    for _ in range(num_platforms):
        x = random.randint(0, SCREEN_WIDTH - PLATFORM_WIDTH_MIN)
        y = random.randint(0, SCREEN_HEIGHT - 100)
        width = random.randint(PLATFORM_WIDTH_MIN, PLATFORM_WIDTH_MAX)
        platform_type = random.choice(["static", "breaking", "disappearing", "broken"])
        platform = Platform(x, y, width, platform_type)
        platform_group.add(platform)

    return player_group, platform_group
