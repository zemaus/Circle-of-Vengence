import pygame, os, sys, math, time, random
from utils import draw_text
class enemy_class(pygame.sprite.Sprite):
    def __init__(self, sprite_location, health=0, attack_power=0, combat_coord=(0,0), alpha=False):
        super().__init__()
        self._attack_power = attack_power
        self._frame = 0
        self._cooldown_timer = 0
        self._time_pass = 0
        self._index = -1
        self._mid_animation = False

        if alpha:
            self.image = pygame.image.load(sprite_location).convert_alpha()
        else:
            self.image = pygame.image.load(sprite_location).convert()
            self.image.set_colorkey((255, 255, 255), pygame.RLEACCEL)

        self.rect = self.image.get_rect()
        self.pos = self.rect.midtop
        self.state = 0 #2 attackin, 1 taking dmg
        self.defending = False
        self.defend_time = 0.1
        self.health = health
        self.combat_coord = combat_coord
        self.dmg_taken = 0
        
    
    def interact(self, dialog, text_box):
        if self._index + 1 >= len(self._dialogs):
            self._index = -1
            return True
        else:
            self._index += 1
        text_box.set_alpha(255)
        log = dialog[self._index]
        draw_text(log, 45, 55, 55, 1490, text_box, (0, 0))
        return False

    def update(self):
        if self.state == 1: # 1 for damaged
            self._mid_animation = True
            move_dist = 2
            if self._frame <= 5:
                self.rect = self.rect.move((move_dist, -move_dist))
            elif self._frame <= 10:
                self.rect = self.rect.move((-move_dist, move_dist))
            elif self._frame <= 30:
                self._mid_animation = False
                self.state = 0
                self._frame = 0
                self.update_location(self.combat_coord)
            self._frame += 1
        elif self.state == 2: # 2 for attacking
            self._mid_animation = True
            move_dist = 10
            if self._frame <= 15:
                self.rect = self.rect.move((-move_dist, move_dist))
            elif self._frame <= 30:
                self.rect = self.rect.move((move_dist, -move_dist))
            else:
                self._mid_animation = False
                self.state = 0
                self._frame = 0
                self.update_location(self.combat_coord)
            self._frame += 1

    def take_damage(self, dmg):
        if not self._mid_animation:
            self.state = 1
        if self.defending:
            dmg = math.floor(dmg/(2/self.defend_time))
        
        self.dmg_taken = dmg
        self.health -= dmg

    def death(self):
        if not self._mid_animation:
            self.state == 3
        self.rotation = 0
        self.original = self.image

    def attacking(self, target):
        if not self._mid_animation:
            self.state = 2
        target.take_damage(self._attack_power)

    def AI_logic(self, enemy, attack_cooldown, defend_frequency, min_defend_interval, max_defend_interval, wait):
        if not self._cooldown_timer:
            self._cooldown_timer = time.time() + wait
            self.attack_cooldown = attack_cooldown
        
        defend_logic = True if round(random.random(), 2) < defend_frequency else False

        if defend_logic: #defend
            self.defend_time = round(random.uniform(min_defend_interval, max_defend_interval), 2)
            self.defending = True
        else:
            self.defend_time = 0
            self.defending = False
        
        if self._time_pass >= self.attack_cooldown: # attack
            self.attacking(enemy)
            self._cooldown_timer = time.time()
            self._time_pass = 0
        else:
            self._time_pass = time.time() - self._cooldown_timer
        
        return self._time_pass

    def update_location(self, coord):
        self.rect.x = coord[0]
        self.rect.y = coord[1]
        self.pos = self.rect.center[0], self.rect.center[1] - self.rect.h