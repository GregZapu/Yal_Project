import pygame
import math
import random
import sqlite3


class Button:
    def __init__(self, text, size, left_up_pos, font_size=96, distance=20):
        self.distance = distance
        self.text = text
        self.size = size
        self.position = left_up_pos
        self.font_size = font_size

    def render(self, screen):
        if player.player_coords[0] >= self.position[0] and player.player_coords[0] < self.position[0] + self.size[0]:
            if player.player_coords[1] >= self.position[1] and player.player_coords[1] < self.position[1] + self.size[1]:
                pygame.draw.rect(screen, (color_for_locations, color_for_locations, color_for_locations), (self.position[0], self.position[1], self.size[0], self.size[1]), width=5)
        font = pygame.font.SysFont(None, self.font_size)
        img = font.render(self.text, True, (color_for_locations, color_for_locations, color_for_locations))
        screen.blit(img, (self.position[0] + self.distance, self.position[1] + self.distance))

class info_bar:
    def __init__(self, entity, size, left_up_pos):
        self.entity = entity
        self.size = size
        self.position = left_up_pos

    def render(self, screen, current_position):
        if self.entity == modul1:
            health_lenth = 42 *  modul1.module_health / modul1.module_max_health
            pygame.draw.rect(screen, "white", (current_position[0] - 20, current_position[1] - 57, self.size[0], self.size[1]), width=3)
            pygame.draw.rect(screen, "white", (current_position[0] - 17, current_position[1] - 54, health_lenth, self.size[1] - 6), width=0)
        if self.entity == modul2:
            health_lenth = 42 *  modul2.module_health / modul2.module_max_health
            pygame.draw.rect(screen, "white", (current_position[0] - 20, current_position[1] - 57, self.size[0], self.size[1]), width=3)
            pygame.draw.rect(screen, "white", (current_position[0] - 17, current_position[1] - 54, health_lenth, self.size[1] - 6), width=0)
        if self.entity == boss:
            health_lenth = 84 *  boss.boss_health / boss.boss_max_health
            pygame.draw.rect(screen, "white", (current_position[0] - 50, current_position[1] - 57, self.size[0], self.size[1]), width=3)
            pygame.draw.rect(screen, "white", (current_position[0] - 47, current_position[1] - 54, health_lenth, self.size[1] - 6), width=0)
        if self.entity == player:
            health_lenth = 34 *  player.player_health / player.player_max_health
            pygame.draw.rect(screen, "white", (player.player_coords[0] - 20, player.player_coords[1] - 35, self.size[0], self.size[1]), width=3)
            pygame.draw.rect(screen, "white", (player.player_coords[0] - 17, player.player_coords[1] - 32, health_lenth, self.size[1] - 6), width=0)


class Player:
    def __init__(self, player_coords):
        self.bouncing = 0
        self.shotgun = 0
        self.homing = 0
        self.player_coords = player_coords
        self.movement_speed = [0, 0]
        self.player_max_health = 100
        self.shot_reload = 0
        self.shot_coldoun = 30
        self.bullet_spread = 0.01
        self.bullet_life_time = 100
        self.player_damage = 15
        self.bullet_speed = 3
        self.way = [0, 0]
        self.aim_dash = False
        self.player_dash = False
        self.movement_direction_history = [[0,0], [0,0], [0,0], [0,0], [0,0], [0,0]]
        self.last_direction = [0, 0]
        self.sprite_counter = 0   
        self.lookng_way = "right"
        self.keys = []
        con = sqlite3.connect("database_for_yal.sqlite")
        cur = con.cursor()
        player_result = cur.execute("""SELECT value FROM Player_stats""").fetchall()
        store_items = cur.execute("""SELECT count FROM Store""").fetchall()
        self.player_max_health = player_result[0][0] * (1 + (store_items[5][0] / 4))
        self.player_health = self.player_max_health
    
    def player_movment(self, movement_button, movment_type):
        global current_location
        global running
        con = sqlite3.connect("database_for_yal.sqlite")
        cur = con.cursor()
        coins = cur.execute("""SELECT count FROM Store WHERE upgrade_name == 'coins'""").fetchall()[0][0]
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
            if movement_button == pygame.K_SPACE and self.player_dash > 0:
                self.aim_dash = True

            if movement_button == pygame.K_e:
                if current_location == "main":
                    if self.player_coords[0] >= 300 and self.player_coords[0] <= 500:
                        if self.player_coords[1] >= 200 and self.player_coords[1] <= 300:
                            location_switch()
                            current_location = "battle"
                if current_location == "main":
                    if self.player_coords[0] >= 300 and self.player_coords[0] <= 500:
                        if self.player_coords[1] >= 460 and self.player_coords[1] <= 560:
                            location_switch()
                            running = False
                if current_location == "main":
                    if self.player_coords[0] >= 300 and self.player_coords[0] <= 500:
                        if self.player_coords[1] >= 330 and self.player_coords[1] <= 430:
                            location_switch()
                            current_location = "store"
                if current_location == "start":
                    if self.player_coords[0] >= 85 and self.player_coords[0] <= 715:
                        if self.player_coords[1] >= 350 and self.player_coords[1] <= 450:
                            location_switch()
                            current_location = "main"
                if current_location == "store":
                    if self.player_coords[0] >= 30 and self.player_coords[0] <= 130:
                        if self.player_coords[1] >= 730 and self.player_coords[1] <= 780:
                            location_switch()
                            current_location = "main"

                    if self.player_coords[0] >= 150 and self.player_coords[0] <= 650 and current_location == 'store':
                        if self.player_coords[1] >= 100 and self.player_coords[1] <= 155:
                            if coins >= 3:
                                con = sqlite3.connect("database_for_yal.sqlite")
                                cur = con.cursor()
                                cur.execute("""UPDATE Store
                                    SET count = count - 3
                                    WHERE upgrade_name == 'coins'""")
                                cur.execute("""UPDATE Store
                                    SET count = count + 1
                                    WHERE upgrade_name == 'bouncing'""")
                                con.commit()
                    if self.player_coords[0] >= 150 and self.player_coords[0] <= 650 and current_location == 'store':
                        if self.player_coords[1] >= 170 and self.player_coords[1] <= 225:
                            if coins >= 1:
                                con = sqlite3.connect("database_for_yal.sqlite")
                                cur = con.cursor()
                                cur.execute("""UPDATE Store
                                    SET count = count - 1
                                    WHERE upgrade_name == 'coins'""")
                                cur.execute("""UPDATE Store
                                    SET count = count + 1
                                    WHERE upgrade_name == 'power_upgrade'""")
                                con.commit()
                    if self.player_coords[0] >= 150 and self.player_coords[0] <= 650 and current_location == 'store':
                        if self.player_coords[1] >= 240 and self.player_coords[1] <= 295:
                            if coins >= 3 and store_items[2][0] == 0:
                                con = sqlite3.connect("database_for_yal.sqlite")
                                cur = con.cursor()
                                cur.execute("""UPDATE Store
                                    SET count = count - 3
                                    WHERE upgrade_name == 'coins'""")
                                cur.execute("""UPDATE Store
                                    SET count = count + 1
                                    WHERE upgrade_name == 'dash_upgrade'""")
                                con.commit()
                    if self.player_coords[0] >= 150 and self.player_coords[0] <= 650 and current_location == 'store':
                        if self.player_coords[1] >= 310 and self.player_coords[1] <= 365:
                            if coins >= 3 and store_items[3][0] == 0:
                                con = sqlite3.connect("database_for_yal.sqlite")
                                cur = con.cursor()
                                cur.execute("""UPDATE Store
                                    SET count = count - 3
                                    WHERE upgrade_name == 'coins'""")
                                cur.execute("""UPDATE Store
                                    SET count = count + 1
                                    WHERE upgrade_name == 'homing_upgrade'""")
                                con.commit()
                    if self.player_coords[0] >= 150 and self.player_coords[0] <= 650 and current_location == 'store':
                        if self.player_coords[1] >= 380 and self.player_coords[1] <= 435:
                            if coins >= 1:
                                con = sqlite3.connect("database_for_yal.sqlite")
                                cur = con.cursor()
                                cur.execute("""UPDATE Store
                                    SET count = count - 1
                                    WHERE upgrade_name == 'coins'""")
                                cur.execute("""UPDATE Store
                                    SET count = count + 1
                                    WHERE upgrade_name == 'range_upgrade'""")
                                con.commit()
                    if self.player_coords[0] >= 150 and self.player_coords[0] <= 650 and current_location == 'store':
                        if self.player_coords[1] >= 450 and self.player_coords[1] <= 505:
                            if coins >= 1:
                                con = sqlite3.connect("database_for_yal.sqlite")
                                cur = con.cursor()
                                cur.execute("""UPDATE Store
                                    SET count = count - 1
                                    WHERE upgrade_name == 'coins'""")
                                cur.execute("""UPDATE Store
                                    SET count = count + 1
                                    WHERE upgrade_name == 'health_upgrade'""")
                                con.commit()
                    if self.player_coords[0] >= 150 and self.player_coords[0] <= 650 and current_location == 'store':
                        if self.player_coords[1] >= 520 and self.player_coords[1] <= 575:
                            if coins >= 1:
                                con = sqlite3.connect("database_for_yal.sqlite")
                                cur = con.cursor()
                                cur.execute("""UPDATE Store
                                    SET count = count - 3
                                    WHERE upgrade_name == 'coins'""")
                                cur.execute("""UPDATE Store
                                    SET count = count + 1
                                    WHERE upgrade_name == 'shotgun'""")
                                con.commit()
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
            if movement_button == pygame.K_SPACE and self.player_dash > 0:
                self.aim_dash = False
                for i in range(1, 14):
                    pygame.draw.circle(screen, (0, 50, 80), (self.player_coords[0] + 10 * i * self.last_direction[0], self.player_coords[1] + 10 * i * self.last_direction [1]), 15)
                
                self.player_coords[0] += 140 * self.last_direction[0]
                self.player_coords[1] += 140 * self.last_direction[1]
            self.keys = pygame.key.get_pressed()
    
    def player_render(self, screen):
        if self.shot_reload > 0:
            self.shot_reload -= 1
        if player.player_coords[0] > 775:
            player.player_coords[0] = 775
        if player.player_coords[1] > 775:
            player.player_coords[1] = 775
        if player.player_coords[0] < 35:
            player.player_coords[0] = 35
        if player.player_coords[1] < 35:
            player.player_coords[1] = 35
        self.sprite_counter += 1
        if movement_speed[0] > 0 or movement_speed[0] == 0 and self.lookng_way == "right"  and movement_speed[1] != 0:
            self.lookng_way = "right"
            if self.sprite_counter <= 10:
                player_right_stand.rect.x = player.player_coords[0] - 25
                player_right_stand.rect.y = player.player_coords[1] - 30
                player_right_stand_group.draw(screen)
            elif self.sprite_counter > 10 and self.sprite_counter <= 20:
                player_right_walk1.rect.x = player.player_coords[0] - 25
                player_right_walk1.rect.y = player.player_coords[1] - 30
                player_right_walk1_group.draw(screen)
            elif self.sprite_counter > 20 and self.sprite_counter <= 30:
                player_right_walk2.rect.x = player.player_coords[0] - 25
                player_right_walk2.rect.y = player.player_coords[1] - 30
                player_right_walk2_group.draw(screen)
        if movement_speed[0] < 0 or movement_speed[0] == 0 and self.lookng_way == "left" and movement_speed[1] != 0:
            self.lookng_way = "left"
            if self.sprite_counter <= 10:
                player_left_stand.rect.x = player.player_coords[0] - 25
                player_left_stand.rect.y = player.player_coords[1] - 30
                player_left_stand_group.draw(screen)
            elif self.sprite_counter > 10 and self.sprite_counter <= 20:
                player_left_walk1.rect.x = player.player_coords[0] - 25
                player_left_walk1.rect.y = player.player_coords[1] - 30
                player_left_walk1_group.draw(screen)
            elif self.sprite_counter > 20 and self.sprite_counter <= 30:
                player_left_walk2.rect.x = player.player_coords[0] - 25
                player_left_walk2.rect.y = player.player_coords[1] - 30
                player_left_walk2_group.draw(screen)
        if movement_speed[0] == 0 and self.lookng_way == "left" and movement_speed[1] == 0:
            player_left_stand.rect.x = player.player_coords[0] - 25
            player_left_stand.rect.y = player.player_coords[1] - 30
            player_left_stand_group.draw(screen)
        if movement_speed[0] == 0 and self.lookng_way == "right" and movement_speed[1] == 0:
            player_right_stand.rect.x = player.player_coords[0] - 25
            player_right_stand.rect.y = player.player_coords[1] - 30
            player_right_stand_group.draw(screen)
        if self.sprite_counter == 30:
            self.sprite_counter = 0

class Module:
    def __init__(self, boss_coords):
        self.module_coords = boss_coords
        self.module_max_health = boss.boss_max_health / 2
        self.module_health = self.module_max_health
        self.bullet_reload = 0
        self.bullet_spread = 0
        self.bullet_life_time = 200
        self.r = 1
        self.y_inert = 0
        self.x_inert = 0
        self.bullet_speed = 1
    
    def module_movement(self):
        t = math.degrees(boss.an) + 90
        t = math.radians(t)

        self.module_coords = [boss.boss_coords[0] + -100 * math.sin(t) * boss.he, boss.boss_coords[1] + 100 * math.cos(t)]

    def module_render(self, screen):
        pygame.draw.circle(screen, (155 / (self.module_max_health / self.module_health) + 100, 0, 0), self.module_coords, 45)

    
class array_Module(Module):
    def module_render(self, screen):
        module2_left.rect.x = self.module_coords[0] - 45
        module2_right.rect.y = self.module_coords[1] - 45
        module2_left.rect.y = self.module_coords[1] - 45
        module2_right.rect.x = self.module_coords[0] - 45
        for i in range(1, 15):
            if self.bullet_reload == 2 * (i + 1):
                bullet = Bullet(self.module_coords, player.player_coords, modul1, -0.15 * (-8 + i))
                bullet_storage.append(bullet)
        if self.bullet_reload == 0:
            self.bullet_reload = 320
            bullet = Bullet(self.module_coords, player.player_coords, modul1, 0.3)
            bullet_storage.append(bullet)

            
        else:
            self.bullet_reload -= 1
        if boss.boss_coords[0] >= player.player_coords[0]:
            module2_left_group.draw(screen)
        else:
            module2_right_group.draw(screen)

class explosion_Module(Module):
    def __init__(self, boss_coords):
        Module.__init__(self, boss_coords)
        self.bullet_life_time = 150
        self.bullet_speed = 1

    def module_movement(self):
        t = math.degrees(boss.an) - 90
        t = math.radians(t)

        self.module_coords = [boss.boss_coords[0] + -100 * math.sin(t) * boss.he, boss.boss_coords[1] + 100 * math.cos(t)]
    def module_render(self, screen):
        module1_left.rect.x = self.module_coords[0] - 45
        module1_right.rect.y = self.module_coords[1] - 45
        module1_left.rect.y = self.module_coords[1] - 45
        module1_right.rect.x = self.module_coords[0] - 45
        if self.bullet_reload == 0:
            self.bullet_reload = 434
            bullet = Bullet(self.module_coords, player.player_coords, modul2, size1=20)
            bullet_storage.append(bullet)
            
        else:
            self.bullet_reload -= 1
        if boss.boss_coords[0] >= player.player_coords[0]:
            module1_left_group.draw(screen)
        else:
            module1_right_group.draw(screen)

class Boss:
    def __init__(self, boss_coords):
        self.boss_coords = boss_coords
        self.bullet_damage = 20
        self.bullet_reload = 0
        self.reload = 60
        self.bullet_spread = 0.1
        self.bullet_life_time = 100
        self.r = 1
        self.an = 1
        self.he = 1
        self.wid = 1
        self.y_inert = 0
        self.x_inert = 0
        self.bullet_speed = 1
        con = sqlite3.connect("database_for_yal.sqlite")
        cur = con.cursor()
        coins = cur.execute("""SELECT count FROM Store WHERE upgrade_name == 'coins'""").fetchall()[0][0]
        player_result = cur.execute("""SELECT value FROM Player_stats""").fetchall()
        boss_result = cur.execute("""SELECT value FROM Boss_stats""").fetchall()
        store_items = cur.execute("""SELECT count FROM Store""").fetchall()
        self.boss_max_health = boss_result[0][0] * (1 + (coins / 4) + (store_items[5][0] / 8)) 
        self.boss_health = self.boss_max_health
    
    def boss_movement(self):
        x_lengh = self.boss_coords[0] - player.player_coords[0]
        y_lengh = self.boss_coords[1] - player.player_coords[1]
        if self.boss_coords[1] > player.player_coords[1]:
            self.he = -1
        else:
            self.he = 1
        if x_lengh != 0:
            self.yx = y_lengh / x_lengh
        else:
            self.yx = y_lengh / 1
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

        if boss.boss_coords[0] > 760:
            boss.boss_coords[0] = 760
        if boss.boss_coords[1] > 760:
            boss.boss_coords[1] = 760
        if boss.boss_coords[0] < 40:
            boss.boss_coords[0] = 40
        if boss.boss_coords[1] < 40:
            boss.boss_coords[1] = 40

    
    def boss_render(self, screen):
        boss_right.rect.x = self.boss_coords[0] - 45
        boss_right.rect.y = self.boss_coords[1] - 45
        boss_left.rect.x = self.boss_coords[0] - 45
        boss_left.rect.y = self.boss_coords[1] - 45
        #pygame.draw.circle(screen, ("green"), self.boss_coords, 50)
        if self.bullet_reload == 0:
            self.bullet_reload = self.reload
            bullet = Bullet(self.boss_coords, player.player_coords, boss)
            bullet_storage.append(bullet)
            bullet = Bullet(self.boss_coords, player.player_coords, boss, 0.3)
            bullet_storage.append(bullet)
            bullet = Bullet(self.boss_coords, player.player_coords, boss, -0.3)
            bullet_storage.append(bullet)
        else:
            self.bullet_reload -= 1
        if boss.boss_coords[0] >= player.player_coords[0]:
            boss_left_group.draw(screen)
        else:
            boss_right_group.draw(screen)

class Bullet:
    def __init__(self, current_pos, end_pos, bullet_owner, ang_ch=0, size1=6):
        self.explosion = False
        self.expl_time = 300
        self.current_pos = current_pos.copy()
        self.effects_pos1 = self.current_pos
        self.effects_pos2 = self.current_pos
        self.effects_pos3 = self.current_pos
        self.effects_pos4 = self.current_pos
        self.effects_pos5 = self.current_pos
        self.effects_pos6 = self.current_pos
        self.bullet_owner = bullet_owner
        self.size = size1
        self.an1 = 0
        self.he1 = 1
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
        pygame.draw.circle(screen, ("green" * (bullet_owner == player) + 'red' * (bullet_owner == boss or bullet_owner == modul1 or bullet_owner == modul2)), (int(self.current_pos[0]), int(self.current_pos[1])), self.size)
            
        
    def render(self, screen):
        
        if self.bullet_owner == player and player.homing:
            x_lengh1 = self.current_pos[0] - boss.boss_coords[0]
            y_lengh1 = self.current_pos[1] - boss.boss_coords[1]
            if self.current_pos[1] > boss.boss_coords[1]:
                self.he1 = -1
            else:
                self.he1 = 1
            if x_lengh1 == 0:
                self.yx1 = 1
            else:
                self.yx1 = y_lengh1 / x_lengh1
            self.g1 = (y_lengh1 ** 2 + x_lengh1 ** 2) ** 0.5
            if self.g1 == 0:
                self.an1 = math.asin(1)
            else:
                self.an1 = math.asin(x_lengh1 / self.g1)
            try:
                self.x_inert += math.sin(self.an1) / self.g1 * 100 * -1 * player.homing
                self.y_inert += math.cos(self.an1) * self.he1 / self.g1 * 100 * 1 * player.homing
            except:
                pass
            #self.inert_g = (self.x_inert ** 2 + self.y_inert ** 2) ** 0.5
        if self.bullet_owner == modul2:
            x_lengh1 = self.current_pos[0] - player.player_coords[0]
            y_lengh1 = self.current_pos[1] - player.player_coords[1]
            if self.current_pos[1] > player.player_coords[1]:
                self.he1 = -1
            else:
                self.he1 = 1
            if x_lengh1 == 0:
                self.yx1 = 1
            else:
                self.yx1 = y_lengh1 / x_lengh1
            self.g1 = (y_lengh1 ** 2 + x_lengh1 ** 2) ** 0.5
            if self.g1 == 0:
                self.an1 = math.asin(1)
            else:
                self.an1 = math.asin(x_lengh1 / self.g1)
            try:
                self.x_inert += math.sin(self.an1) / self.g1 * 100 * -1
                self.y_inert += math.cos(self.an1) * self.he1 / self.g1 * 100 * 1
            except:
                pass
            self.inert_g = (self.x_inert ** 2 + self.y_inert ** 2) ** 0.5

            if self.inert_g > 6:
                self.x_inert /= self.inert_g / 6
                self.y_inert /= self.inert_g / 6
            #self.inert_g = (self.x_inert ** 2 + self.y_inert ** 2) ** 0.5dd


        if self.lifetime >= 0:
            self.current_pos[0] += self.bullet_owner.bullet_speed * math.sin(self.an) * 5 * -1 + self.x_inert + (self.bullet_owner == modul2) * math.sin(self.an1) * - 2
            self.current_pos[1] += self.bullet_owner.bullet_speed * math.cos(self.an) * 5 * self.he + self.y_inert + (self.bullet_owner == modul2) * math.cos(self.an1) * 2 * self.he1
        try:
            pygame.draw.circle(screen, ("green" * (self.bullet_owner == player) + 'red' * (self.bullet_owner == boss) + 'orange' * (self.bullet_owner == modul1 or self.bullet_owner == modul2)), (int(self.current_pos[0]), int(self.current_pos[1])), self.size)
        except:
            pass
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
            if self.bullet_owner == modul2:
                self.explosion = True
                
                pygame.draw.circle(screen, (148, 212, 163), (self.current_pos), self.size - 3)

                g = ((self.current_pos[0] - player.player_coords[0]) ** 2 +  (self.current_pos[1] - player.player_coords[1]) ** 2) ** 0.5
                if g <= 160:
                    player.player_health -= 45
                    pygame.draw.circle(screen, (105, 214, 130), (self.current_pos), self.size - 1)
            else:
                self.bullet_appear = False
        if (self.current_pos[0] - modul2.module_coords[0] >= -38) and (self.current_pos[0] - modul2.module_coords[0]) <= 38 and self.bullet_owner == player and module_render2 == True and current_location == 'battle':
            if self.current_pos[1] - modul2.module_coords[1] >= -38 and self.current_pos[1] - modul2.module_coords[1] <= 38:
                self.bullet_appear = False
                modul2.module_health -= player.player_damage
        if (self.current_pos[0] - modul1.module_coords[0] >= -38) and (self.current_pos[0] - modul1.module_coords[0]) <= 38 and self.bullet_owner == player and module_render1 == True and current_location == 'battle':
            if self.current_pos[1] - modul1.module_coords[1] >= -38 and self.current_pos[1] - modul1.module_coords[1] <= 38:
                self.bullet_appear = False
                modul1.module_health -= player.player_damage
        if self.current_pos[0] - boss.boss_coords[0] >= -38 and self.current_pos[0] - boss.boss_coords[0] <= 38 and self.bullet_owner == player and boss_render == True and current_location == 'battle':
            if self.current_pos[1] - boss.boss_coords[1] >= -38 and self.current_pos[1] - boss.boss_coords[1] <= 38:
                self.bullet_appear = False
                boss.boss_health -= player.player_damage
        if self.current_pos[0] - player.player_coords[0] >= -11 - self.size and self.current_pos[0] - player.player_coords[0] <= 11 + self.size and (self.bullet_owner == boss or self.bullet_owner == modul1):
            if self.current_pos[1] - player.player_coords[1] >= -11 - self.size and self.current_pos[1] - player.player_coords[1] <= 11 + self.size:
                self.bullet_appear = False
                player.player_health -= boss.bullet_damage
                
        if ((self.current_pos[0] < 0) or (self.current_pos[0] > 800)) and self.bullet_owner == player and player.bouncing > 0:
            self.x_inert *= -1
            self.an = - self.an

        if ((self.current_pos[1] < 0) or (self.current_pos[1] > 800)) and self.bullet_owner == player and player.bouncing > 0:
            self.y_inert *= -1
            degreeee = math.degrees(self.an)
            self.an = math.radians(-degreeee + 180)



def location_switch():
    global color_for_locations
    while color_for_locations > 1:
        color_for_locations -= 2
        if current_location == "main":
            main_menu()
        if current_location == "start":
            start_location()
        if current_location == "store":
            store_location()


def store_location():
    global running
    global bullet_appear
    global boss_render
    global module_render1
    global module_render2
    
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
            if player.shotgun > 0:
                
                end_pos = [pos[0], pos[1]]
                bullet_appear = True
                bullet = Bullet(player.player_coords, end_pos, player) 
                bullet_storage.append(bullet)
                bullet = Bullet(player.player_coords, end_pos, player, 0.07) 
                bullet_storage.append(bullet)
                bullet = Bullet(player.player_coords, end_pos, player, 0.14) 
                bullet_storage.append(bullet)
                bullet = Bullet(player.player_coords, end_pos, player, -0.07)
                bullet_storage.append(bullet)
                bullet = Bullet(player.player_coords, end_pos, player, -0.14) 
                bullet_storage.append(bullet)
                player.shot_reload = player.shot_coldoun
            else:
                end_pos = [pos[0], pos[1]]
                bullet_appear = True
                bullet = Bullet(player.player_coords, end_pos, player) 
                bullet_storage.append(bullet)
                player.shot_reload = player.shot_coldoun

    store_exit_button.render(screen)
    Bouncing_upgrade_button.render(screen)
    Power_upgrade_button.render(screen)
    Dash_upgrade_button.render(screen)
    Homing_upgrade_button.render(screen)
    Range_upgrade_button.render(screen)
    Health_upgrade_button.render(screen)
    Shotgun_upgrade_button.render(screen)
    

    player.player_coords[0] += movement_speed[0]
    player.player_coords[1] += movement_speed[1]
    player.player_render(screen)


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

    con = sqlite3.connect("database_for_yal.sqlite")
    cur = con.cursor()
    coins = cur.execute("""SELECT count FROM Store WHERE upgrade_name == 'coins'""").fetchall()[0][0]
    font = pygame.font.SysFont(None, 40)
    img = font.render('Coins: ' + str(coins), True, (color_for_locations, color_for_locations, color_for_locations))
    screen.blit(img, (670, 760))

    pygame.display.flip()
    clock.tick(50)


def start_location():
    global running
    global bullet_appear
    global boss_render
    global module_render1
    global module_render2
    
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
            if player.shotgun > 0:
                
                end_pos = [pos[0], pos[1]]
                bullet_appear = True
                bullet = Bullet(player.player_coords, end_pos, player) 
                bullet_storage.append(bullet)
                bullet = Bullet(player.player_coords, end_pos, player, 0.07) 
                bullet_storage.append(bullet)
                bullet = Bullet(player.player_coords, end_pos, player, 0.14) 
                bullet_storage.append(bullet)
                bullet = Bullet(player.player_coords, end_pos, player, -0.07)
                bullet_storage.append(bullet)
                bullet = Bullet(player.player_coords, end_pos, player, -0.14) 
                bullet_storage.append(bullet)
                player.shot_reload = player.shot_coldoun
            else:
                end_pos = [pos[0], pos[1]]
                bullet_appear = True
                bullet = Bullet(player.player_coords, end_pos, player) 
                bullet_storage.append(bullet)
                player.shot_reload = player.shot_coldoun

    first_button.render(screen)

    player.player_coords[0] += movement_speed[0]
    player.player_coords[1] += movement_speed[1]
    player.player_render(screen)


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

def main_menu():
    global running
    global bullet_appear
    global boss_render
    global module_render1
    global module_render2
    global start_boss_coordinates

    
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
            if player.shotgun > 0:
                
                end_pos = [pos[0], pos[1]]
                bullet_appear = True
                bullet = Bullet(player.player_coords, end_pos, player) 
                bullet_storage.append(bullet)
                bullet = Bullet(player.player_coords, end_pos, player, 0.07) 
                bullet_storage.append(bullet)
                bullet = Bullet(player.player_coords, end_pos, player, 0.14) 
                bullet_storage.append(bullet)
                bullet = Bullet(player.player_coords, end_pos, player, -0.07)
                bullet_storage.append(bullet)
                bullet = Bullet(player.player_coords, end_pos, player, -0.14) 
                bullet_storage.append(bullet)
                player.shot_reload = player.shot_coldoun
            else:
                end_pos = [pos[0], pos[1]]
                bullet_appear = True
                bullet = Bullet(player.player_coords, end_pos, player) 
                bullet_storage.append(bullet)
                player.shot_reload = player.shot_coldoun

    start_button.render(screen)
    store_button.render(screen)
    exit_button.render(screen)

    player.player_coords[0] += movement_speed[0]
    player.player_coords[1] += movement_speed[1]
    player.player_render(screen)


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
    con = sqlite3.connect("database_for_yal.sqlite")
    cur = con.cursor()

    if boss.boss_health <= 0:
        cur.execute("""UPDATE Store
            SET count = count + 1
            WHERE upgrade_name == 'coins'""")
    
    coins = cur.execute("""SELECT count FROM Store WHERE upgrade_name == 'coins'""").fetchall()[0][0]
    player.shotgun = cur.execute("""SELECT count FROM Store WHERE upgrade_name == 'shotgun'""").fetchall()[0][0]
    player_result = cur.execute("""SELECT value FROM Player_stats""").fetchall()
    boss_result = cur.execute("""SELECT value FROM Boss_stats""").fetchall()
    store_items = cur.execute("""SELECT count FROM Store""").fetchall()
    player.player_max_health = player_result[0][0] * (1 + (store_items[5][0] / 4))
    player.shot_coldoun = player_result[1][0]
    player.player_damage = 15 * (1 + (store_items[1][0] / 4))
    player.bullet_spread = player_result[2][0] / (1 + (store_items[1][0] / 4))
    player.bullet_life_time = player_result[3][0] * (1 + (store_items[4][0] / 4))
    player.bouncing = store_items[0][0]
    player.homing = store_items[3][0]
    player.player_dash = store_items[2][0]
    boss.boss_max_health = boss_result[0][0] * (1 + (coins / 4) + (store_items[5][0] / 8))
    boss.bullet_damage = boss_result[2][0] * (1 + (coins / 4))
    boss.reload = boss_result[3][0]
    boss.bullet_life_time = boss_result[4][0] * (1 + (coins / 4))
    boss.bullet_spread = boss_result[5][0] / (1 + (coins / 4))
    boss.bullet_speed = boss_result[6][0]
    boss.boss_health = boss.boss_max_health
    player.player_health = player.player_max_health
    modul1.module_health = modul1.module_max_health
    modul2.module_health = modul2.module_max_health
    module_render1 = True
    module_render2 = True
    boss_render = True
    start_boss_coordinates = [400, 700]
    
    con.commit()

    pygame.display.flip()
    clock.tick(50)


def battle_field():
    global running
    global bullet_appear
    global boss_render
    global module_render1
    global module_render2
    global current_location
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
            if player.shotgun > 0:
                end_pos = [pos[0], pos[1]]
                bullet_appear = True
                bullet = Bullet(player.player_coords, end_pos, player) 
                bullet_storage.append(bullet)
                bullet = Bullet(player.player_coords, end_pos, player, 0.07) 
                bullet_storage.append(bullet)
                bullet = Bullet(player.player_coords, end_pos, player, 0.14) 
                bullet_storage.append(bullet)
                bullet = Bullet(player.player_coords, end_pos, player, -0.07)
                bullet_storage.append(bullet)
                bullet = Bullet(player.player_coords, end_pos, player, -0.14) 
                bullet_storage.append(bullet)
                player.shot_reload = player.shot_coldoun
            else:
                end_pos = [pos[0], pos[1]]
                bullet_appear = True
                bullet = Bullet(player.player_coords, end_pos, player) 
                bullet_storage.append(bullet)
                player.shot_reload = player.shot_coldoun
        
    player.player_coords[0] += movement_speed[0]
    player.player_coords[1] += movement_speed[1]
    player.player_render(screen)
    player_healthbar.render(screen, player.player_coords)
    if module_render1 and boss_render == True and player.player_dash >0:
        module_healthbar1.render(screen, modul1.module_coords)
        modul1.module_movement()
        modul1.module_render(screen)
    if module_render2 and boss_render == True and player.homing >0:
        module_healthbar2.render(screen, modul2.module_coords)
        modul2.module_movement()
        modul2.module_render(screen)
    if boss_render == True:
        boss.boss_movement() 
        boss.boss_render(screen)
        boss_healthbar.render(screen, boss.boss_coords)
    if boss.boss_health <= 0:
        module_render1 = False
        module_render2 = False
        boss_render = False
        current_location = "main"
        main_menu()
    if player.player_health <= 0:
        boss_render = False
        current_location = "main"
        main_menu()
    if modul1.module_health <= 0:
            module_render1 = False
    if modul2.module_health <= 0:
        module_render2 = False

    if not player.way == [0, 0]:
        p = player.way[::]
        player.movement_direction_history.append(p)

        player.movement_direction_history = player.movement_direction_history[-5:]

    player.last_direction = player.movement_direction_history[-3]

            
    if player.aim_dash:
        pygame.draw.circle(screen, ("white"), (player.player_coords[0] + 140 * player.last_direction[0], player.player_coords[1] + 140 * player.last_direction[1]), 6)
    for elem in bullet_storage:
            if elem.bullet_appear == True:
                if elem.bullet_owner == modul2:
                    pygame.draw.circle(screen, ('white'), (elem.current_pos), elem.expl_time / 2, 2)
                    if elem.explosion and elem.expl_time >= 0:
                        pygame.draw.circle(screen, ('red'), (elem.current_pos), 150 - (elem.expl_time / 2))
                        elem.expl_time -= 30
                        elem.explosion = True
                    if elem.expl_time <0 and elem.explosion:
                        elem.bullet_appear = False
                elem.render(screen)
            else:
                if not elem.bullet_owner == modul2:
                    bullet_storage.remove(elem)

    pygame.display.flip()
    clock.tick(50)

if __name__ == '__main__': 
    pygame.init()
    pygame.display.set_caption('Тестовое')
    size = width, height = 800, 800
    screen = pygame.display.set_mode(size)
    running = True
    boss_render = True
    module_render1 = True
    module_render2 = True
    bullet_storage = []
    current_location = "start"
    color_for_locations = 255

    v = 20  # пикселей в секунду
    fps = 60
    clock = pygame.time.Clock()

    start_player_coords = [200, 200]
    start_boss_coordinates = [400, 700]
    movement_speed = [0, 0]
    player = Player(start_player_coords)
    boss = Boss(start_boss_coordinates)
    modul1 = array_Module(start_boss_coordinates)
    modul2 = explosion_Module(start_boss_coordinates)
    module_healthbar1 = info_bar(modul1, (45, 10), (200, 50))
    module_healthbar2 = info_bar(modul2, (45, 10), (200, 80))

    first_button = Button("Press E to interact", [630, 100], [85, 350])
    start_button = Button("Start", [200, 100], [300, 200])
    store_button = Button("Store", [200, 100], [300, 330])
    exit_button = Button("Exit", [200, 100], [300, 460])
    store_exit_button = Button("Exit", [100, 50], [30, 730], 54, 10)
    Bouncing_upgrade_button = Button("Bouncing upgrade - 3 coins", [500, 55], [150, 100], 54, 10)
    Power_upgrade_button = Button("Power upgrade - 1 coin", [500, 55], [150, 170], 54, 10)
    Dash_upgrade_button = Button("Dash upgrade - 3 coins", [500, 55], [150, 240], 54, 10)
    Homing_upgrade_button = Button("Homing upgrade - 3 coins", [500, 55], [150, 310], 54, 10)
    Range_upgrade_button = Button("Range upgrade - 1 coin", [500, 55], [150, 380], 54, 10)
    Health_upgrade_button = Button("Health upgrade - 1 coin", [500, 55], [150, 450], 54, 10)
    Shotgun_upgrade_button = Button("Shotgun upgrade - 3 coins", [500, 55], [150, 520], 54, 10)

    #работа с бд
    con = sqlite3.connect("database_for_yal.sqlite")
    cur = con.cursor()
    coins = cur.execute("""SELECT count FROM Store WHERE upgrade_name == 'coins'""").fetchall()[0][0]
    player_result = cur.execute("""SELECT value FROM Player_stats""").fetchall()
    boss_result = cur.execute("""SELECT value FROM Boss_stats""").fetchall()
    store_items = cur.execute("""SELECT count FROM Store""").fetchall()
    player.player_max_health = player_result[0][0] * (1 + (store_items[5][0] / 4))
    player.shotgun = cur.execute("""SELECT count FROM Store WHERE upgrade_name == 'shotgun'""").fetchall()[0][0]
    player.shot_coldoun = player_result[1][0]
    player.player_damage = 15 * (1 + (store_items[1][0] / 4))
    player.bullet_spread = player_result[2][0] / (1 + (store_items[1][0] / 4))
    player.bullet_life_time = player_result[3][0] * (1 + (store_items[4][0] / 4))
    player.bullet_speed = player_result[4][0] * (1 + (store_items[0][0] / 4))
    player.homing = store_items[3][0]
    player.player_dash = store_items[2][0]
    boss.boss_max_health = boss_result[0][0] * (1 + (coins / 4) + (store_items[5][0] / 8))
    boss.bullet_damage = boss_result[2][0] * (1 + (coins / 4))
    boss.reload = boss_result[3][0]
    boss.bullet_life_time = boss_result[4][0] * (1 + (coins / 4))
    boss.bullet_spread = boss_result[5][0] / (1 + (coins / 4))
    boss.bullet_speed = boss_result[6][0]
    player.bouncing = store_items[0][0]

    boss_healthbar = info_bar(boss, (90, 10), (200, 10))
    player_healthbar = info_bar(player, (40, 10), (10, 10))
    # спрайты
    boss_left_group = pygame.sprite.Group()
    boss_right_group = pygame.sprite.Group()

    module1_left_group = pygame.sprite.Group()
    module1_right_group = pygame.sprite.Group()
    module2_left_group = pygame.sprite.Group()
    module2_right_group = pygame.sprite.Group()

    player_left_stand_group = pygame.sprite.Group()
    player_right_stand_group = pygame.sprite.Group()
    player_left_walk1_group = pygame.sprite.Group()
    player_right_walk1_group = pygame.sprite.Group()
    player_left_walk2_group = pygame.sprite.Group()
    player_right_walk2_group = pygame.sprite.Group()

    boss_left = pygame.sprite.Sprite()
    boss_right = pygame.sprite.Sprite()

    player_left_stand = pygame.sprite.Sprite()
    player_right_stand = pygame.sprite.Sprite()
    player_left_walk1 = pygame.sprite.Sprite()
    player_right_walk1 = pygame.sprite.Sprite()
    player_left_walk2 = pygame.sprite.Sprite()
    player_right_walk2 = pygame.sprite.Sprite()
    module1_left = pygame.sprite.Sprite()
    module1_right = pygame.sprite.Sprite()
    module2_left = pygame.sprite.Sprite()
    module2_right = pygame.sprite.Sprite()

    module1_left.image = pygame.image.load("Assets/Sprite_module_left_for_pj.png")
    module1_right.image = pygame.image.load("Assets/Sprite_module_right_for_pj.png")
    module2_left.image = pygame.image.load("Assets/Sprite_module2_left_for_pj.png")
    module2_right.image = pygame.image.load("Assets/Sprite_module2_right_for_pj.png")

    boss_left.image = pygame.image.load("Assets/Sprite_boss_left_for_pj.png")
    boss_right.image = pygame.image.load("Assets/Sprite_boss_right_for_pj.png")
    player_left_stand.image = pygame.image.load("Assets/Sprite_player_left_for_pj.png")
    player_right_stand.image = pygame.image.load("Assets/Sprite_player_right_for_pj.png")
    player_left_walk1.image = pygame.image.load("Assets/Sprite_player1_left_for_pj.png")
    player_right_walk1.image = pygame.image.load("Assets/Sprite_player1_right_for_pj.png")
    player_left_walk2.image = pygame.image.load("Assets/Sprite_player2_left_for_pj.png")
    player_right_walk2.image = pygame.image.load("Assets/Sprite_player2_right_for_pj.png")

    module1_left.rect = module1_left.image.get_rect()
    module1_right.rect = module1_right.image.get_rect()
    module2_left.rect = module2_left.image.get_rect()
    module2_right.rect = module2_right.image.get_rect()

    boss_left.rect = boss_left.image.get_rect()
    boss_right.rect = boss_right.image.get_rect()
    player_left_stand.rect = player_left_stand.image.get_rect()
    player_right_stand.rect = player_right_stand.image.get_rect()
    player_left_walk1.rect = player_left_walk1.image.get_rect()
    player_right_walk1.rect = player_left_walk1.image.get_rect()
    player_left_walk2.rect = player_left_walk1.image.get_rect()
    player_right_walk2.rect = player_left_walk1.image.get_rect()
    
    module1_left_group.add(module1_left)
    module1_right_group.add(module1_right)
    module2_left_group.add(module2_left)
    module2_right_group.add(module2_right)

    player_left_stand_group.add(player_left_stand)
    player_right_stand_group.add(player_right_stand)
    player_left_walk1_group.add(player_left_walk1)
    player_right_walk1_group.add(player_right_walk1)
    player_left_walk2_group.add(player_left_walk2)
    player_right_walk2_group.add(player_right_walk2)
    boss_left_group.add(boss_left)
    boss_right_group.add(boss_right)
    while running:
        if current_location == "start":
            start_location()
            color_for_locations = 255
        if current_location == "main":
            main_menu()
            color_for_locations = 255
        if current_location == "battle":
            battle_field()
            color_for_locations = 255
        if current_location == "store":
            store_location()
            color_for_locations = 255
    pygame.quit()
