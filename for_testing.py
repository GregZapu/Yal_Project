import pygame
import math
from copy import copy



class Bullet:
    def __init__(self, current_pos, end_pos):
        self.current_pos = current_pos.copy()
        self.end_pos = end_pos
        self.bullet_appear = True
        self.modifyers =  [1, 1]
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

    character_coordinates = [200, 200]
    boss_coordinates = [500, 500]
    movement_speed = [0, 0]
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                end_pos = [event.pos[0], event.pos[1]]
                bullet_appear = True
                bullet = Bullet(character_coordinates, end_pos) 
                bullet_storage.append(bullet)          

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    movement_speed[1] -= 10
                if event.key == pygame.K_s:
                    movement_speed[1] += 10
                if event.key == pygame.K_a:
                    movement_speed[0] -= 10
                if event.key == pygame.K_d:
                    movement_speed[0] += 10
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    movement_speed[1] += 10
                if event.key == pygame.K_s:
                    movement_speed[1] -= 10
                if event.key == pygame.K_a:
                    movement_speed[0] += 10
                if event.key == pygame.K_d:
                    movement_speed[0] -= 10

        character_coordinates[0] += movement_speed[0]
        character_coordinates[1] += movement_speed[1]

        if character_coordinates[0] > boss_coordinates[0]:
            boss_coordinates[0] += 2
        elif character_coordinates[0] < boss_coordinates[0]:
            boss_coordinates[0] -= 2
        if character_coordinates[1] > boss_coordinates[1]:
            boss_coordinates[1] += 2
        elif character_coordinates[1] < boss_coordinates[1]:
            boss_coordinates[1] -= 2     
        for elem in bullet_storage:
            if elem.bullet_appear == True:
                elem.render(screen)
            else:
                bullet_storage.remove(elem)
        pygame.draw.circle(screen, (0, 0, 255), character_coordinates, 20)
        pygame.draw.circle(screen, "green", boss_coordinates, 20)
        pygame.display.flip()
        clock.tick(50)
    pygame.quit()


#pygame.draw.circle(screen, (0, 0, 255), character_coordinates, 20)
