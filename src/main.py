import pygame
from .scenes.scene_manager import SceneManager


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("оп, отсылка на Нико")

    manager = SceneManager(screen)
    manager.run()

    pygame.quit()


if __name__ == "__main__":
    main()
