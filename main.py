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
            map_generator(self.difficulty, self.difficulty)
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
                elif level == 'easy':
                    self.difficulty = 64
                    self.choose_dif_playing = False
                elif level == 'medium':
                    self.difficulty = 110
                    self.choose_dif_playing = False
                elif level == 'hardcore':
                    self.difficulty = 180
                    self.choose_dif_playing = False
                elif level == 'instruction':
                    self.instruction_playing = False
                elif level == 'bye':
                    self.quit()

        else:
            pygame.draw.rect(self.screen, defaultcolor, (x, y, width, height))

        self.button_text = self.small_font.render(message, True, BLACK)
        self.screen.blit(self.button_text, (x + (width - self.button_text.get_width()) / 2, y + (height - self.button_text.get_height()) / 2))

    def show_start_screen(self):
        self.big_font = pygame.font.SysFont("comicsansms", 200)
        self.font = pygame.font.SysFont("comicsansms", 100)
        self.small_font = pygame.font.SysFont("comicsansms", 50)
        self.start_text = self.big_font.render("aMAZEing", True, ORCHID)
        self.start_screen_playing = True

        while self.start_screen_playing:
            self.screen.fill(BACKGROUND_COLOR)
            self.screen.blit(self.start_text, ((WIDTH - self.start_text.get_width()) / 2, 60))

            self.create_button("LET'S GO", WIDTH / 2 - 150, HEIGHT / 2, 300, 100, WHITE, LIGHTPURPLE, 0)

            self.events()

            pygame.display.update()
            self.clock.tick(FPS)

    def choose_map(self):
        self.choose_a_map_text = self.font.render("Which map do you want?", True, ORCHID)
        self.choose_screen_playing = True

        while self.choose_screen_playing:
            self.screen.fill(BACKGROUND_COLOR)
            self.screen.blit(self.choose_a_map_text, ((WIDTH - self.choose_a_map_text.get_width()) / 2, 60))

            self.create_button("Download my map", 50, HEIGHT / 2, 350, 100, WHITE, LIGHTPURPLE, 1)

            self.create_button("Make me a map", WIDTH - 400, HEIGHT / 2, 350, 100, WHITE, LIGHTPURPLE, 2)

            self.events()

            pygame.display.update()
            self.clock.tick(FPS)

    def instruction_download(self):
        self.instruction_text1 = self.small_font.render("Add your map as map.txt file.", True, ORCHID)
        self.instruction_text2 = self.small_font.render("Make sure, that the file consists", True, ORCHID)
        self.instruction_text3 = self.small_font.render("only of the next symbols:", True, ORCHID)
        self.instruction_text4 = self.small_font.render("1 - stands for a wall", True, ORCHID)
        self.instruction_text5 = self.small_font.render(". - stands for a cell", True, ORCHID)
        self.instruction_text6 = self.small_font.render("S - stands for start position", True, ORCHID)
        self.instruction_text7 = self.small_font.render("F - stands for finish", True, ORCHID)

        self.instruction_playing = True

        while self.instruction_playing:
            self.screen.fill(BACKGROUND_COLOR)
            self.screen.blit(self.instruction_text1, ((WIDTH - self.instruction_text1.get_width()) / 2, 20))
            self.screen.blit(self.instruction_text2, ((WIDTH - self.instruction_text2.get_width()) / 2, 60))
            self.screen.blit(self.instruction_text3, ((WIDTH - self.instruction_text3.get_width()) / 2, 100))
            self.screen.blit(self.instruction_text4, ((WIDTH - self.instruction_text4.get_width()) / 2, 140))
            self.screen.blit(self.instruction_text5, ((WIDTH - self.instruction_text5.get_width()) / 2, 180))
            self.screen.blit(self.instruction_text6, ((WIDTH - self.instruction_text6.get_width()) / 2, 220))
            self.screen.blit(self.instruction_text7, ((WIDTH - self.instruction_text7.get_width()) / 2, 260))

            self.create_button("Done", WIDTH / 2 - 150, HEIGHT - 300, 300, 100, WHITE, LIGHTPURPLE, 'instruction')

            self.events()

            pygame.display.update()
            self.clock.tick(FPS)

    def choose_difficulty(self):
        self.choose_dif_text = self.font.render("Choose difficulty", True, ORCHID)
        self.choose_dif_playing = True

        while self.choose_dif_playing:
            self.screen.fill(BACKGROUND_COLOR)
            self.screen.blit(self.choose_dif_text, ((WIDTH - self.choose_dif_text.get_width()) / 2, 100))

            self.create_button("EASY", 100, HEIGHT / 2 + 100, 250, 100, WHITE, LIGHTPURPLE, 'easy')

            self.create_button("MEDIUM", WIDTH / 2 - 125, HEIGHT / 2 + 100, 250, 100, WHITE, LIGHTPURPLE, 'medium')

            self.create_button("HARDCORE", WIDTH - 350, HEIGHT / 2 + 100, 250, 100, WHITE, LIGHTPURPLE, 'hardcore')

            self.events()

            pygame.display.update()
            self.clock.tick(FPS)

    def show_go_screen(self):
        self.go_text = self.font.render("YOU ARE AWESOME!!!", True, ORCHID)
        self.go_playing = True

        while self.go_playing:
            self.screen.fill(BLACK)
            self.screen.blit(self.go_text, ((WIDTH - self.go_text.get_width()) / 2, 250))

            self.create_button("I'M AWESOME!!", WIDTH / 2 - 200, HEIGHT / 2 + 75, 400, 100, WHITE, LIGHTPURPLE, 'bye')

            self.events()

            pygame.display.update()
            self.clock.tick(FPS)


game = Game()
game.show_start_screen()
game.choose_map()
if game.make_me_a_map:
    game.choose_difficulty()
else:
    game.instruction_download()
game.new()
game.run()
game.show_go_screen()

