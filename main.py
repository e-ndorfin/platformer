from pygame.locals import *
import pygame
import sys
import os

clock = pygame.time.Clock()

pygame.init()

pygame.display.set_caption('Platformer')

WINDOW_SIZE = (600, 400)
PLAYER_SIZE = (50, 50)

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)

# render player onto this image, and then scale it onto the window
display = pygame.Surface((300, 200))

player_location = [50, 50]
player_y_momentum = 0
air_timer = 0

playerImage = pygame.image.load(os.path.join('Assets', 'player.png')).convert()
# gets rid of white, sets it transparent
playerImage.set_colorkey((255, 255, 255))
player = pygame.Rect(player_location[0], player_location[1],
                     playerImage.get_width(), playerImage.get_height())
testCollision = pygame.Rect(100, 100, 100, 50)

grassImage = pygame.image.load(os.path.join('Assets', 'personal', 'grass.png'))
dirtImage = pygame.image.load(os.path.join('Assets', 'personal', 'dirt.png'))
TILE_SIZE = grassImage.get_width()


def load_map(path):
    game_map = []
    f = open('map.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    for row in data:
        game_map.append(list(row))
    return game_map


game_map = load_map('map')


def collisionTest(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


def handleMovement(rect, movement, tiles):  # movement = x, y
    # tracks directino that player is colliding with object
    collision_types = {'top': False, 'bottom': False,
                       'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collisionTest(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:  # moving right
            rect.right = tile.left  # when the player collides with right tile
            collision_types['right'] = True
        elif movement[0] < 0:  # moving left
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collisionTest(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types


moving_right = False
moving_left = False

while True:
    display.fill((146, 244, 255))

    tile_rects = []
    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                display.blit(dirtImage, (x * TILE_SIZE, y * TILE_SIZE))
            if tile == '2':
                display.blit(grassImage, (x * TILE_SIZE, y * TILE_SIZE))
            if tile != '0':
                tile_rects.append(pygame.Rect(
                    x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            x += 1
        y += 1

    player_movement = [0, 0]
    if moving_right:
        player_movement[0] += 2
    if moving_left:
        player_movement[0] -= 2
    player_movement[1] += player_y_momentum
    player_y_momentum += 0.2

    if player_y_momentum > 3:  # caps fall speed
        player_y_momentum = 3

    player, collisions = handleMovement(player, player_movement, tile_rects)
    if collisions['bottom']:
        player_y_momentum = 0
        air_timer = 0
    else:
        air_timer += 1
    if collisions['top']:
        player_y_momentum = 0

    display.blit(playerImage, (player.x, player.y))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP:
                if air_timer < 6:
                    player_y_momentum -= 5
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False

    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf, (0, 0))

    pygame.display.update()
    clock.tick(60)
