# levels.py

import random
from sprites import Platform

class LevelManager:
    def __init__(self, diff):
        self.diff = diff

    def generate_platforms(self, platform_group):
        y = 800
        while y > 0:
            x = random.randint(0, 500)
            moving = random.choice([True, False])
            platform_group.add(Platform(x, y, moving))
            y -= 100
