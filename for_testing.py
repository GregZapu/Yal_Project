import pygame
import math
import random


class info_bar:
    def __init__(self, entity, size, left_up_pos):
        self.entity = entity
        self.size = size
        self.position = left_up_pos

    def render(self, screen):
        if self.entity == boss:
            health_lenth = 494 *  boss.boss_health / 500
            pygame.draw.rect(screen, "white", (self.position[0], self.position[1], self.size[0], self.size[1]), width=3)
            pygame.draw.rect(screen, "white", (self.position[0] + 3, self.position[1] + 3, health_lenth, self.size[1] - 6), width=0)

        if self.entity == player:
            health_lenth = 94 *  player.player_health / 45
            pygame.draw.rect(screen, "white", (self.position[0], self.position[1], self.size[0], self.size[1]), width=3)
            pygame.draw.rect(screen, "white", (self.position[0] + 3, self.position[1] + 3, health_lenth, self.size[1] - 6), width=0)


class Player:
    def __init__(self, player_coords):
        self.homing = True
        self.player_coords = player_coords
        self.movement_speed = [0, 0]
        self.player_health = 45
        self.shot_reload = 0
        self.bullet_spread = 0.01
        self.bullet_life_time = 100
        self.bullet_speed = 2
        self.way = [0, 0]
        self.aim_dash = False
        self.movement_direction_history = [[0,0], [0,0], [0,0], [0,0], [0,0], [0,0]]
        self.last_direction = [0, 0]   
    
    def player_movment(self, movement_button, movment_type):
        if movment_type == pygame.KEYDOWN:
            if movement_button == pygame.K_w:
                movement_speed[1] -= 5
                self.way[1] -= 1
            if movement_button == pygame.K_s:
                movement_speed[1] += 5
                self.way[1] += 1
            if movement_button == pygame.K_a:
                movement_speed[0] -= 5
                self.way[0] -= 1
            if movement_button == pygame.K_d:
                movement_speed[0] += 5
                self.way[0] += 1
            if movement_button == pygame.K_SPACE:
                self.aim_dash = True
                
        elif movment_type == pygame.KEYUP:
            if movement_button == pygame.K_w:
                movement_speed[1] += 5
                self.way[1] += 1
            if movement_button == pygame.K_s:
                movement_speed[1] -= 5
                self.way[1] -= 1
            if movement_button == pygame.K_a:
                movement_speed[0] += 5
                self.way[0] += 1
            if movement_button == pygame.K_d:
                movement_speed[0] -= 5
                self.way[0] -= 1
            if movement_button == pygame.K_SPACE:
                self.aim_dash = False
                for i in range(1, 14):
                    pygame.draw.circle(screen, (0,0,112), (self.player_coords[0] + 10 * i * self.last_direction[0], self.player_coords[1] + 10 * i * self.last_direction [1]), 15)
                
                self.player_coords[0] += 140 * self.last_direction[0]
                self.player_coords[1] += 140 * self.last_direction[1]
    
    def player_render(self, screen):
        if self.shot_reload > 0:
            self.shot_reload -= 1
        pygame.draw.circle(screen, ("blue"), self.player_coords, 20)

class Boss:
    def __init__(self, boss_coords):
        self.boss_coords = boss_coords
        self.boss_health = 500
        self.bullet_reload = 0
        self.bullet_spread = 0.1
        self.bullet_life_time = 200
        self.r = 1
        self.y_inert = 0
        self.x_inert = 0
        self.bullet_speed = 1
    
    def boss_movement(self):
        x_lengh = self.boss_coords[0] - player.player_coords[0]
        y_lengh = self.boss_coords[1] - player.player_coords[1]
        if self.boss_coords[1] > player.player_coords[1]:
            self.he = -1
        else:
            self.he = 1
        self.yx = y_lengh / x_lengh
        self.g = (y_lengh ** 2 + x_lengh ** 2) ** 0.5
        self.an = math.asin(x_lengh / self.g)
        if self.g < 650:
            self.r = -1
        elif self.g > 650:
            self.r = 1
        #if self.g > 500:
        self.x_inert += 1 * math.sin(self.an) * 5 * -1 * 0.002 * ((self.g / 100 ) ** 2)
        self.y_inert += math.cos(self.an) * 5 * self.he * 0.002 * ((self.g / 100 ) ** 2)
        self.inert_g = (self.x_inert ** 2 + self.y_inert ** 2) ** 0.5

        if self.inert_g > 6:
            self.x_inert /= self.inert_g / 6
            self.y_inert /= self.inert_g / 6
        self.boss_coords[0] += self.x_inert + (1 * math.sin(self.an) * 5 * -1 * self.r * 0.6) 
        self.boss_coords[1] += self.y_inert + (math.cos(self.an) * 5 * self.he * self.r * 0.6) 

    
    def boss_render(self, screen):
        pygame.draw.circle(screen, ("green"), self.boss_coords, 50)
        if self.bullet_reload == 0:
            self.bullet_reload = 60
            bullet = Bullet(self.boss_coords, player.player_coords, boss)
            bullet_storage.append(bullet)
            bullet = Bullet(self.boss_coords, player.player_coords, boss, 0.3)
            bullet_storage.append(bullet)
            bullet = Bullet(self.boss_coords, player.player_coords, boss, -0.3)
            bullet_storage.append(bullet)
        else:
            self.bullet_reload -= 1

class Bullet:
    def __init__(self, current_pos, end_pos, bullet_owner, ang_ch=0, size1=6):
        self.current_pos = current_pos.copy()
        self.effects_pos1 = self.current_pos
        self.effects_pos2 = self.current_pos
        self.effects_pos3 = self.current_pos
        self.effects_pos4 = self.current_pos
        self.effects_pos5 = self.current_pos
        self.effects_pos6 = self.current_pos
        self.bullet_owner = bullet_owner
        self.size = size1
        self.x_inert = 0
        self.y_inert = 0
    
        self.end_pos = end_pos
        
        self.bullet_appear = True
        self.lifetime = bullet_owner.bullet_life_time
        x_lengh = self.current_pos[0] - self.end_pos[0]
        y_lengh = self.current_pos[1] - self.end_pos[1]
        self.ang_ch = ang_ch
        try:
            self.yx = y_lengh / x_lengh
            self.g = (y_lengh ** 2 + x_lengh ** 2) ** 0.5
            if current_pos[1] > end_pos[1]:
                self.he = -1
            else:
                self.he = 1
            self.an = math.asin(x_lengh / self.g) + random.uniform(- bullet_owner.bullet_spread, bullet_owner.bullet_spread) + self.ang_ch
        except:
            self.bullet_appear = False
        pygame.draw.circle(screen, ("green"), (int(self.current_pos[0]), int(self.current_pos[1])), self.size)
            
        
    def render(self, screen):
        if self.bullet_owner == player and player.homing:
            x_lengh1 = self.current_pos[0] - boss.boss_coords[0]
            y_lengh1 = self.current_pos[1] - boss.boss_coords[1]
            if self.current_pos[1] > boss.boss_coords[1]:
                self.he1 = -1
            else:
                self.he1 = 1
            self.yx1 = y_lengh1 / x_lengh1
            self.g1 = (y_lengh1 ** 2 + x_lengh1 ** 2) ** 0.5
            self.an1 = math.asin(x_lengh1 / self.g1)
            self.x_inert += math.sin(self.an1) / self.g1 * 100 * -1
            self.y_inert += math.cos(self.an1) * self.he1 / self.g1 * 100 * 1
            #self.inert_g = (self.x_inert ** 2 + self.y_inert ** 2) ** 0.5

        self.current_pos[0] += self.bullet_owner.bullet_speed * math.sin(self.an) * 5 * -1 + self.x_inert
        self.current_pos[1] += self.bullet_owner.bullet_speed * math.cos(self.an) * 5 * self.he + self.y_inert
        pygame.draw.circle(screen, ("green"), (int(self.current_pos[0]), int(self.current_pos[1])), self.size)
        self.effects_pos6 = self.effects_pos5
        self.effects_pos5 = self.effects_pos4
        self.effects_pos4 = self.effects_pos3
        self.effects_pos3 = self.effects_pos2
        self.effects_pos2 = self.effects_pos1
        self.effects_pos1 = self.current_pos.copy()
        pygame.draw.circle(screen, (105, 214, 130), (self.effects_pos3), self.size - 1)
        pygame.draw.circle(screen, (121, 212, 142), (self.effects_pos5), self.size - 2)
        pygame.draw.circle(screen, (148, 212, 163), (self.effects_pos6), self.size - 3)
        self.lifetime -= 1
        if self.lifetime == 0:
            self.bullet_appear = False
        if self.current_pos[1] == self.end_pos[1] and self.current_pos[0] == self.end_pos[0]:
            self.bullet_appear = False
        if self.current_pos[0] - boss.boss_coords[0] >= -38 and self.current_pos[0] - boss.boss_coords[0] <= 38 and self.bullet_owner == player and boss_render == True:
            if self.current_pos[1] - boss.boss_coords[1] >= -38 and self.current_pos[1] - boss.boss_coords[1] <= 38:
                self.bullet_appear = False
                boss.boss_health -= 15
        if self.current_pos[0] - player.player_coords[0] >= -15 and self.current_pos[0] - player.player_coords[0] <= 15 and self.bullet_owner == boss:
            if self.current_pos[1] - player.player_coords[1] >= -15 and self.current_pos[1] - player.player_coords[1] <= 15:
                self.bullet_appear = False
                player.player_health -= 15

        

if __name__ == '__main__': 
    pygame.init()
    pygame.display.set_caption('Тестовое')
    size = width, height = 800, 800
    screen = pygame.display.set_mode(size)
    running = True
    boss_render = True
    bullet_storage = []

    v = 20  # пикселей в секунду
    fps = 60
    clock = pygame.time.Clock()

    start_player_coords = [200, 200]
    start_boss_coordinates = [700, 700]
    movement_speed = [0, 0]
    player = Player(start_player_coords)
    boss = Boss(start_boss_coordinates)
    boss_healthbar = info_bar(boss, (500, 30), (200, 10))
    player_healthbar = info_bar(player, (100, 10), (10, 10))
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                player.player_movment(event.key, event.type)
        pressed = pygame.mouse.get_pressed()
        pos = pygame.mouse.get_pos()
        if pressed[0]:
            if player.shot_reload == 0:
                
                end_pos = [pos[0], pos[1]]
                bullet_appear = True
                bullet = Bullet(player.player_coords, end_pos, player) 
                bullet_storage.append(bullet)
                player.shot_reload = 30
        
        player.player_coords[0] += movement_speed[0]
        player.player_coords[1] += movement_speed[1]
        player.player_render(screen)
        player_healthbar.render(screen)
        if boss_render == True:
            boss.boss_movement() 
            boss.boss_render(screen)
            boss_healthbar.render(screen)
        if boss.boss_health <= 0:
            boss_render = False
        if not player.way == [0, 0]:
            p = player.way[::]
            player.movement_direction_history.append(p)

            player.movement_direction_history = player.movement_direction_history[-5:]

        player.last_direction = player.movement_direction_history[-3]

            
        if player.aim_dash:
                pygame.draw.circle(screen, ("white"), (player.player_coords[0] + 140 * player.last_direction[0], player.player_coords[1] + 140 * player.last_direction[1]), 6)
        for elem in bullet_storage:
            if elem.bullet_appear == True:
                elem.render(screen)
            else:
                bullet_storage.remove(elem)
        pygame.display.flip()
        clock.tick(50)
    pygame.quit()
