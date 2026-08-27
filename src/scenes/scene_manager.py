import pygame
from PIL import Image

from src.cat import Cat
from src.config import settings

INTRO = 0
NAME_INPUT = 1
FEEDING = 2
STATUS = 3
RESTART = 4


def load_gif_frames(filename):
    gif = Image.open(filename)
    frames = []
    durations = []

    try:
        while True:
            frame = gif.convert("RGBA")
            raw = frame.tobytes()
            surface = pygame.image.frombytes(raw, frame.size, "RGBA")
            surface = pygame.transform.scale(surface, (800, 600))
            frames.append(surface)

            durations.append(gif.info.get('duration', 100))

            gif.seek(gif.tell() + 1)
    except EOFError:
        pass

    return frames, durations


def get_gif_frame(elapsed, durations, total_duration, loop):
    if loop:
        elapsed = elapsed % total_duration
    elif elapsed >= total_duration:
        return None, elapsed

    accumulated = 0
    for i, duration in enumerate(durations):
        accumulated += duration
        if elapsed < accumulated:
            return i, elapsed

    return len(durations) - 1, elapsed


class SceneManager:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True

        self.background = [
            pygame.transform.scale(pygame.image.load(f"{settings.BASE_PATH_BACKGROUND}first_date.png"), (800, 600)),
            pygame.transform.scale(pygame.image.load(f"{settings.BASE_PATH_BACKGROUND}feed_cat.png"), (800, 600))
        ]

        self.font = pygame.font.SysFont('Arial', 36)
        self.small_font = pygame.font.SysFont('Arial', 24)

        self.start_frames, self.start_durations = load_gif_frames(f"{settings.BASE_PATH_BACKGROUND}start.gif")
        self.end_frames, self.end_durations = load_gif_frames(f"{settings.BASE_PATH_BACKGROUND}end.gif")
        self.start_total = sum(self.start_durations)
        self.end_total = sum(self.end_durations)

        self.state = INTRO
        self.cat = None
        self.user_input_name = ""
        self.feed_choice = None
        self.restart_choice = None

        self.intro_timer = 0
        self.end_timer = 0
        self.status_timer = 0

        self.cat_x = 50
        self.cat_speed = 0.2
        self.cat_dir = 1

        self.rect_feed_yes = pygame.Rect(250, 300, 120, 50)
        self.rect_feed_no = pygame.Rect(430, 300, 120, 50)
        self.rect_restart_yes = pygame.Rect(250, 400, 120, 50)
        self.rect_restart_no = pygame.Rect(430, 400, 120, 50)

    def run(self):
        while self.running:
            delta_ms = self.clock.tick(60)
            events = pygame.event.get()
            self.handle_events(events)
            self.update(delta_ms)
            self.draw()
            pygame.display.flip()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

            if self.state == NAME_INPUT and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and self.user_input_name.strip():
                    self.cat.rename(self.user_input_name.strip())
                    self.user_input_name = ""
                    self.state = FEEDING
                    self.feed_choice = None
                elif event.key == pygame.K_BACKSPACE:
                    self.user_input_name = self.user_input_name[:-1]
                else:
                    if len(self.user_input_name) < 15 and event.unicode.isprintable():
                        self.user_input_name += event.unicode

            if self.state == FEEDING and event.type == pygame.MOUSEBUTTONDOWN and self.feed_choice is None:
                if self.rect_feed_yes.collidepoint(event.pos):
                    self.feed_choice = True
                elif self.rect_feed_no.collidepoint(event.pos):
                    self.feed_choice = False

            if self.state == RESTART and event.type == pygame.MOUSEBUTTONDOWN and self.restart_choice is None:
                if self.rect_restart_yes.collidepoint(event.pos):
                    self.restart_choice = True
                elif self.rect_restart_no.collidepoint(event.pos):
                    self.restart_choice = False

            if (self.state == STATUS and self.status_timer > 500) and \
                (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN):
                    if self.cat and self.cat.life <= 0:
                        self.state = RESTART
                        self.restart_choice = None
                        self.end_timer = 0
                    else:
                        self.state = FEEDING
                        self.feed_choice = None
                    break

    def update(self, delta_ms):
        if self.state == INTRO:
            self.intro_timer += delta_ms
            frame_result = get_gif_frame(self.intro_timer, self.start_durations,
                                         self.start_total, False)
            frame_index = frame_result[0]
            if frame_index is None:
                self.state = NAME_INPUT
                self.intro_timer = 0
                self.cat = Cat()

        elif self.state == FEEDING:
            if self.feed_choice is not None:
                self.cat.feed(self.feed_choice)
                self.cat.live()
                self.state = STATUS
                self.status_timer = 0

        elif self.state == STATUS:
            self.status_timer += delta_ms
            self.cat_x = (self.cat_x + self.cat_speed * delta_ms) % self.screen.get_width()

        elif self.state == RESTART:
            self.end_timer += delta_ms
            if self.restart_choice is not None:
                if self.restart_choice:
                    self.cat = None
                    self.user_input_name = ""
                    self.feed_choice = None
                    self.restart_choice = None
                    self.intro_timer = 0
                    self.end_timer = 0
                    self.state = INTRO
                else:
                    self.running = False

    def draw(self):
        self.screen.fill((255, 255, 255))

        if self.state == INTRO:
            frame_result = get_gif_frame(self.intro_timer, self.start_durations,
                                         self.start_total, False)
            frame_index = frame_result[0]
            if frame_index is not None:
                self.screen.blit(self.start_frames[frame_index], (0, 0))

        elif self.state == NAME_INPUT:
            self.screen.blit(self.background[0], (0, 0))
            if self.cat:
                self.cat.draw_cat(self.screen)
            text = self.font.render("Вы нашли кота, как назовёте?", True, (0, 0, 0))
            self.screen.blit(text, (150, 50))
            current_time = pygame.time.get_ticks()
            cursor = "|" if current_time % 800 < 400 else ""
            input_surface = self.font.render(self.user_input_name + cursor, True, (0, 0, 0))
            self.screen.blit(input_surface, (300, 250))

        elif self.state == FEEDING:
            self.screen.blit(self.background[1], (0, 0))
            if self.cat:
                self.cat.draw_cat(self.screen)
            question = self.font.render("Покормить кота?", True, (255, 255, 255), (0, 0, 0))
            self.screen.blit(question, (280, 200))

            pygame.draw.rect(self.screen, (0, 150, 0), self.rect_feed_yes)
            yes_text = self.font.render("Да", True, (255, 255, 255))
            self.screen.blit(yes_text, (self.rect_feed_yes.x + 40, self.rect_feed_yes.y + 12))

            pygame.draw.rect(self.screen, (150, 0, 0), self.rect_feed_no)
            no_text = self.font.render("Нет", True, (255, 255, 255))
            self.screen.blit(no_text, (self.rect_feed_no.x + 40, self.rect_feed_no.y + 12))

        elif self.state == STATUS:
            self.screen.blit(self.background[1], (0, 0))
            if self.cat:
                name_text = self.font.render(f"Имя: {self.cat.name}", True, (255, 255, 255))
                self.screen.blit(name_text, (50, 30))
                life_text = self.small_font.render(f"Здоровье: {self.cat.life}", True, self.cat.color)
                hungry_text = self.small_font.render(f"Голод: {self.cat.hungry}", True, (200, 200, 200))
                self.screen.blit(life_text, (50, 80))
                self.screen.blit(hungry_text, (50, 110))
                colored_skin = self.cat.get_colored_skin()
                self.screen.blit(colored_skin, (self.cat_x, 100))
                self.screen.blit(colored_skin, (self.cat_x - self.screen.get_width(), 100))
                if self.status_timer > 500:
                    hint = self.small_font.render("нажмите что бы перейти далее", True, (180, 180, 180))
                    self.screen.blit(hint, (250, 500))

        elif self.state == RESTART:
            frame_result = get_gif_frame(self.end_timer, self.end_durations,
                                         self.end_total, True)
            frame_index = frame_result[0]
            self.screen.blit(self.end_frames[frame_index], (0, 0))

            if self.cat:
                gray_skin = pygame.transform.grayscale(self.cat.skin)
                self.screen.blit(gray_skin, (30, 50))

            over_text = self.font.render("Кот уснул навсегда...", True, (255, 0, 0))
            self.screen.blit(over_text, (220, 20))
            ask_text = self.font.render("Попробовать ещё раз?", True, (255, 255, 255))
            self.screen.blit(ask_text, (250, 350))

            pygame.draw.rect(self.screen, (0, 150, 0), self.rect_restart_yes)
            yes_text = self.font.render("Да", True, (255, 255, 255))
            self.screen.blit(yes_text, (self.rect_restart_yes.x + 40, self.rect_restart_yes.y + 12))

            pygame.draw.rect(self.screen, (150, 0, 0), self.rect_restart_no)
            no_text = self.font.render("Нет", True, (255, 255, 255))
            self.screen.blit(no_text, (self.rect_restart_no.x + 40, self.rect_restart_no.y + 12))