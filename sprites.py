from settings import *
import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x_spawn, y_spawn):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.image.fill(ORCHID)
        self.rect = self.image.get_rect()
        self.rect.x = x_spawn * CELL_SIZE
        self.rect.y = y_spawn * CELL_SIZE

        self.speedx = 0
        self.speedy = 0

    def update(self):
        self.speedx = 0
        self.speedy = 0
        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_LEFT] or key_state[pygame.K_a]:
            self.speedx = -PLAYER_SPEED
        if key_state[pygame.K_RIGHT] or key_state[pygame.K_d]:
            self.speedx = PLAYER_SPEED
        if key_state[pygame.K_UP] or key_state[pygame.K_w]:
            self.speedy = -PLAYER_SPEED
        if key_state[pygame.K_DOWN] or key_state[pygame.K_s]:
            self.speedy = PLAYER_SPEED

        self.rect.x += self.speedx
        self.collide_with_walls('horizontal')
        self.rect.y += self.speedy
        self.collide_with_walls('vertical')
        self.collide_with_finish()


    def collide_with_walls(self, direction):
        if direction == 'horizontal':
            hits = pygame.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.speedx > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.speedx < 0:
                    self.rect.x = hits[0].rect.right
                self.speedx = 0

        if direction == 'vertical':
            hits = pygame.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.speedy > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.speedy < 0:
                    self.rect.y = hits[0].rect.bottom
                self.speedy = 0

    def collide_with_finish(self):
        hits = pygame.sprite.spritecollide(self, self.game.finish, False)
        if hits:
            self.game.playing = False


class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x_spawn, y_spawn):
        self.groups = game.all_sprites, game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()

        self.rect.x = x_spawn * CELL_SIZE
        self.rect.y = y_spawn * CELL_SIZE


class Finish(pygame.sprite.Sprite):
    def __init__(self, game, x_spawn, y_spawn):
        self.groups = game.all_sprites, game.finish
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()

        self.rect.x = x_spawn * CELL_SIZE
        self.rect.y = y_spawn * CELL_SIZE


