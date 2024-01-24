import pygame
import math


class info_bar:
    def __init__(self, entity, size, left_up_pos):
        self.entity = entity
        self.size = size
        self.position = left_up_pos

    def render(self, screen):
        if self.entity == boss:
            health_lenth = 494 *  boss.boss_helath / 1000
            pygame.draw.rect(screen, "white", (self.position[0], self.position[1], self.size[0], self.size[1]), width=3)
            pygame.draw.rect(screen, "white", (self.position[0] + 3, self.position[1] + 3, health_lenth, self.size[1] - 6), width=0)


class Player:
    def __init__(self, player_coords):
        self.player_coords = player_coords
        self.movement_speed = [0, 0]
        self.player_health = 100
        self.shot_reload = 0
    
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
        if self.shot_reload > 0:
            self.shot_reload -= 1
        pygame.draw.circle(screen, ("blue"), self.player_coords, 20)

class Boss:
    def __init__(self, boss_coords):
        self.boss_coords = boss_coords
        self.boss_helath = 1000
    
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
    def __init__(self, current_pos, end_pos, bullet_owner):
        self.current_pos = current_pos.copy()
        self.effects_pos1 = self.current_pos
        self.effects_pos2 = self.current_pos
        self.effects_pos3 = self.current_pos
        self.effects_pos4 = self.current_pos
        self.effects_pos5 = self.current_pos
        self.effects_pos6 = self.current_pos
        self.bullet_owner = bullet_owner

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
        pygame.draw.circle(screen, ("green"), (int(self.current_pos[0]), int(self.current_pos[1])), 5)
            
        
    def render(self, screen):
        self.current_pos[0] += 1 * math.sin(self.an) * 5 * -1
        self.current_pos[1] += 1 * math.cos(self.an) * 5 * self.he
        pygame.draw.circle(screen, ("green"), (int(self.current_pos[0]), int(self.current_pos[1])), 5)
        self.effects_pos6 = self.effects_pos5
        self.effects_pos5 = self.effects_pos4
        self.effects_pos4 = self.effects_pos3
        self.effects_pos3 = self.effects_pos2
        self.effects_pos2 = self.effects_pos1
        self.effects_pos1 = self.current_pos.copy()
        pygame.draw.circle(screen, (105, 214, 130), (self.effects_pos3), 4)
        pygame.draw.circle(screen, (121, 212, 142), (self.effects_pos5), 3)
        pygame.draw.circle(screen, (148, 212, 163), (self.effects_pos6), 2)
        self.lifetime -= 1
        if self.lifetime == 0:
            self.bullet_appear = False
        if self.current_pos[1] == self.end_pos[1] and self.current_pos[0] == self.end_pos[0]:
            self.bullet_appear = False
        if self.current_pos[0] - boss.boss_coords[0] >= -10 and self.current_pos[0] - boss.boss_coords[0] <= 10:
            if self.current_pos[1] - boss.boss_coords[1] >= -10 and self.current_pos[1] - boss.boss_coords[1] <= 10:
                self.bullet_appear = False
                boss.boss_helath -= 15

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
    boss_healthbar = info_bar(boss, (500, 30), (200, 10))
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if player.shot_reload == 0:
                    end_pos = [event.pos[0], event.pos[1]]
                    bullet_appear = True
                    bullet = Bullet(player.player_coords, end_pos, player) 
                    bullet_storage.append(bullet)
                    player.shot_reload = 100

            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                player.player_movment(event.key, event.type)

        player.player_coords[0] += movement_speed[0]
        player.player_coords[1] += movement_speed[1]
        player.player_render(screen)

        boss.boss_movement() 
        boss.boss_render(screen)
        boss_healthbar.render(screen)

        for elem in bullet_storage:
            if elem.bullet_appear == True:
                elem.render(screen)
            else:
                bullet_storage.remove(elem)
        pygame.display.flip()
        clock.tick(50)
    pygame.quit()

