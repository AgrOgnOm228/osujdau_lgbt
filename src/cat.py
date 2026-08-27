import random
from pathlib import Path

import pygame

from src.config import settings


class Cat:
    name = None

    def __init__(self):
        self.life = 100
        self.hungry = 0
        self.skin = self._get_random_skin()

        self.color = (0, 255, 0)
        self.update_color()

    def rename(self, name):
        self.name = name

    @staticmethod
    def _get_random_skin():
        cat_skin_name = []
        folder_path = Path(settings.BASE_PATH_CAT)
        for item in folder_path.iterdir():
            cat_skin_name.append(item.name)

        SKIN_LINK = f"{settings.BASE_PATH_CAT}{random.choice(cat_skin_name)}"
        print(SKIN_LINK)
        return pygame.image.load(SKIN_LINK)

    def update_color(self):
        if self.life > 80:
            self.color = (0, 255, 0)
        elif self.life > 50:
            self.color = (255, 255, 0)
        else:
            self.color = (255, 0, 0)

    def feed(self, user_choice):
        if user_choice:
            self.hungry += 30
        else:
            self.hungry -= 10

    def live(self):
        self.hungry -= 10
        if self.hungry <= 0:
            self.life -= 20
        self.update_color()

    def get_colored_skin(self):
        surface = self.skin.copy()
        surface.fill(self.color, special_flags=pygame.BLEND_RGB_MULT)
        return surface

    def draw_cat(self, screen):
        screen.blit(self.skin, (300, 100))
