import pygame
import sys
from os import path
from settings import *
from map import Map
from sprites import Player, Wall, Finish
from camera import Camera
from map_generator import map_generator



class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

    def load_map(self):
        folder = path.dirname(__file__)
        if self.make_me_a_map:  # Если False, то надо подгрузить самому
            map_generator(64, 64)
        self.map = Map(path.join(folder, 'map.txt'))

    def new(self):
        self.load_map()
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.finish = pygame.sprite.Group()
        for row, cells in enumerate(self.map.data):
            for col, cell in enumerate(cells):
                if cell == '1':
                    Wall(self, col, row)
                if cell == 'S':
                    self.player = Player(self, col, row)
                if cell == 'F':
                    Finish(self, col, row)

        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pygame.quit()
        sys.exit()

    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)

    def draw_grid(self):
        for x in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, DARKBLUE, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, DARKBLUE, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.draw_grid()
        for sprite in self.all_sprites:
           self.screen.blit(sprite.image, self.camera.apply(sprite))
        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

    def create_button(self, message, x, y, width, height, hovercolor, defaultcolor, level):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed(3)
        if x + width > mouse[0] > x and y + height > mouse[1] > y:
            pygame.draw.rect(self.screen, hovercolor, (x, y, width, height))
            if click[0] == 1:
                if level == 0:
                    self.start_screen_playing = False
                elif level == 1:
                    self.make_me_a_map = False
                    self.choose_screen_playing = False
                elif level == 2:
                    self.make_me_a_map = True
                    self.choose_screen_playing = False

        else:
            pygame.draw.rect(self.screen, defaultcolor, (x, y, width, height))

        self.start_button_text = self.small_font.render(message, True, BLACK)
        self.screen.blit(self.start_button_text, (x + 38, y + 15))


    def show_start_screen(self): 
        self.font = pygame.font.SysFont("comicsansms", 80)
        self.small_font = pygame.font.SysFont("comicsansms", 40)
        self.start_text = self.font.render("aMAZEing", True, ORCHID)
        self.start_screen_playing = True

        while self.start_screen_playing:
            self.screen.fill(BACKGROUND_COLOR)
            self.screen.blit(self.start_text, ((WIDTH - self.start_text.get_width()) / 2, 0))

            self.create_button("LET'S GO", (WIDTH - 200) / 2, (HEIGHT - 50) / 2, 200, 50, WHITE, LIGHTGREY, 0)

            self.events()  # мб заменить придётся

            pygame.display.update()
            self.clock.tick(FPS)

    def choose_map(self):
        self.choose_a_map_text = self.font.render("Which map do you want?", True, ORCHID)
        self.choose_screen_playing = True

        while self.choose_screen_playing:
            self.screen.fill(BACKGROUND_COLOR)
            self.screen.blit(self.choose_a_map_text, ((WIDTH - self.choose_a_map_text.get_width()) / 2, 0))

            self.create_button("Download my map", 100, (HEIGHT - 50) / 2, 300, 100, WHITE, LIGHTGREY, 1)

            self.create_button("Make me a map", WIDTH - 400, (HEIGHT - 50) / 2, 300, 100, WHITE, LIGHTGREY, 2)

            self.events()  # мб заменить придётся

            pygame.display.update()
            self.clock.tick(FPS)

    def show_go_screen(self):  #TODO
        pass


game = Game()
game.show_start_screen()
game.choose_map()
game.new()
game.run()
game.show_go_screen()

