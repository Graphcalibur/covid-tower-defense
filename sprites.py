from settings import *
from tilemap import collide_hit_rect, round_to_tilesize, tile_from_coords, tile_from_xcoords
from enemies import *

import random

vec = pg.math.Vector2

def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y


class Start():
    def __init__(self, game, x, y, w, h, spawn_rate):
        self.game = game
        self.x = x
        self.y = y
        self.rect = pg.Rect(x, y, w, h)
        self.rect.x = x
        self.rect.y = y
        self.next_spawn = pg.time.get_ticks()
        self.spawn_rate = spawn_rate

    def update(self):
        if (pg.time.get_ticks() >= self.next_spawn):
            Enemy(self.game, self.x, self.y, tile_from_xcoords(self.game.goal.x), tile_from_xcoords(self.game.goal.y), random.randint(50, 150), random.randint(5, 15), ENEMY_IMG)
            self.next_spawn = pg.time.get_ticks() + self.spawn_rate * 1000


class Goal():
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.rect = pg.Rect(x, y, w, h)
        self.rect.x = x
        self.rect.y = y

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.obstacles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.rect = pg.Rect(x, y, TILESIZE, TILESIZE)
        self.game.map.change_node(tile_from_xcoords(x), tile_from_xcoords(y), 1)
