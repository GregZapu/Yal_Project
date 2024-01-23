import pygame
import math
from copy import copy


class Player:
    def __init__(self, player_coords):
        self.player_coords = player_coords
        self.movement_speed = [0, 0]
    
    def player_movment(self, movement_button, movment_type):
        if movment_type == pygame.KEYDOWN:
            if movement_button == pygame.K_w:
                movement_speed[1] -= 10
            if movement_button == pygame.K_s:
                movement_speed[1] += 10
            if movement_button == pygame.K_a:
                movement_speed[0] -= 10
            if movement_button == pygame.K_d:
                movement_speed[0] += 10
        elif movment_type == pygame.KEYUP:
            if movement_button == pygame.K_w:
                movement_speed[1] += 10
            if movement_button == pygame.K_s:
                movement_speed[1] -= 10
            if movement_button == pygame.K_a:
                movement_speed[0] += 10
            if movement_button == pygame.K_d:
                movement_speed[0] -= 10
    
    def player_render(self, screen):
        pygame.draw.circle(screen, ("blue"), self.player_coords, 20)

class Boss:
    def __init__(self, boss_coords):
        self.boss_coords = boss_coords
    
    def boss_movement(self):
        if player.player_coords[0] > self.boss_coords[0]:
            self.boss_coords[0] += 2
        elif player.player_coords[0] < self.boss_coords[0]:
            self.boss_coords[0] -= 2
        if player.player_coords[1] > self.boss_coords[1]:
            self.boss_coords[1] += 2
        elif player.player_coords[1] < self.boss_coords[1]:
            self.boss_coords[1] -= 2
    
    def boss_render(self, screen):
        pygame.draw.circle(screen, ("green"), self.boss_coords, 20)

class Bullet:
    def __init__(self, current_pos, end_pos):
        self.current_pos = current_pos.copy()
        self.end_pos = end_pos
        self.bullet_appear = True
        self.lifetime = 60
        x_lengh = self.current_pos[0] - self.end_pos[0]
        y_lengh = self.current_pos[1] - self.end_pos[1]
        try:
            self.yx = y_lengh / x_lengh
            self.g = (y_lengh ** 2 + x_lengh ** 2) ** 0.5
            if current_pos[1] > end_pos[1]:
                self.he = -1
            else:
                self.he = 1
            self.an = math.asin(x_lengh / self.g)
        except:
            self.bullet_appear = False
            
        
    def render(self, screen):
        pygame.draw.circle(screen, ("green"), (int(self.current_pos[0]), int(self.current_pos[1])), 5)
        self.current_pos[0] += 1 * math.sin(self.an) * 5 * -1
        self.current_pos[1] += 1 * math.cos(self.an) * 5 * self.he
        self.lifetime -= 1
        if self.lifetime == 0:
            self.bullet_appear = False
        if self.current_pos[1] == self.end_pos[1] and self.current_pos[0] == self.end_pos[0]:
            self.bullet_appear = False

if __name__ == '__main__': 
    pygame.init()
    pygame.display.set_caption('Тестовое')
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)
    running = True
    bullet_storage = []

    v = 20  # пикселей в секунду
    fps = 60
    clock = pygame.time.Clock()

    start_player_coords = [200, 200]
    start_boss_coordinates = [100, 100]
    movement_speed = [0, 0]
    player = Player(start_player_coords)
    boss = Boss(start_boss_coordinates)
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                end_pos = [event.pos[0], event.pos[1]]
                bullet_appear = True
                bullet = Bullet(player.player_coords, end_pos) 
                bullet_storage.append(bullet)          

            if event.type == pygame.KEYDOWN:
                player.player_movment(event.key, event.type)
            if event.type == pygame.KEYUP:
                player.player_movment(event.key, event.type)

        player.player_coords[0] += movement_speed[0]
        player.player_coords[1] += movement_speed[1]
        player.player_render(screen)

        boss.boss_movement() 
        boss.boss_render(screen)

        for elem in bullet_storage:
            if elem.bullet_appear == True:
                elem.render(screen)
            else:
                bullet_storage.remove(elem)
        pygame.display.flip()
        clock.tick(50)
    pygame.quit()

