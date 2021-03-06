import pygame, os, sys, math
os.chdir('../game')

class player_class(pygame.sprite.Sprite):
    def __init__(self, health, attack_power):
        super().__init__()
        self._player_state = [os.path.join('assets', 'player', 'normal_player.png'), 
                            os.path.join('assets', 'player', 'damaged_player.png'),
                            os.path.join('assets', 'player', 'attacking_player.png')]
        
        self._attack_power = attack_power
        self._dir = 0 #0 for left, 1 for right
        self._frame = 0
        self.state = 0
        self.dmg_taken = 0
        self.health = health
        self.defending = False
        self.defend_time = 0.1
        
        self.image = pygame.image.load(self._player_state[0]).convert()
        self.image.set_colorkey((255, 255, 255), pygame.RLEACCEL)
        self.rect = self.image.get_rect()
        self.pos = self.rect.midtop

    def update(self):
        if self.state == 2: # 2 for attacking
            move_dist = 10
            if self._frame <= 15:
                self.rect = self.rect.move((move_dist, -move_dist))
            elif self._frame <= 30:
                self.rect = self.rect.move((-move_dist, move_dist))
            else:
                self.change_state(0)
                self._frame = 0
            self._frame += 1
        elif self.state == 1: # 1 for damaged
            move_dist = 2
            if self._frame <= 5:
                self.rect = self.rect.move((-move_dist, move_dist))
            elif self._frame <= 10:
                self.rect = self.rect.move((move_dist, -move_dist))
            elif self._frame <= 30:
                self.change_state(0)
                self._frame = 0

            self._frame += 1

    def take_damage(self, dmg):
        self.change_state(1)
        if self.defending:
            dmg = math.floor(dmg/(2/self.defend_time))
        
        self.health -= dmg
        self.dmg_taken = dmg


    def attacking(self, target):
        self.change_state(2)
        target.take_damage(self._attack_power)


    def change_state(self, state_int):
        self.image = pygame.image.load(self._player_state[state_int]).convert()
        self.image.set_colorkey((255, 255, 255), pygame.RLEACCEL)
        self.state = state_int

    def movement(self):
        keys = pygame.key.get_pressed()
        speed = 10
        if keys[pygame.K_d]: # right key
            if not self._dir: 
                self.image = pygame.transform.flip(self.image, 1, 0)
                self._dir = 1
            self.rect = self.rect.move((speed, 0))
        elif keys[pygame.K_a]: # left key
            if self._dir:
                self.image = pygame.transform.flip(self.image, 1, 0)
                self._dir = 0
            self.rect = self.rect.move((-speed, 0))

    def update_location(self, x, y):
        self.rect.move_ip(x, y)
        self.pos = self.rect.midtop


def main():
    pygame.init()
    screen = pygame.display.set_mode((1600,900))
    pygame.display.set_caption("Test_player")

    background = pygame.image.load(os.path.join('assets','scene1', 'background.png')).convert()
    screen.blit(background, (0, 0))
    pygame.display.flip()

    user = player_class(10, 10, 10)
    sprites = pygame.sprite.RenderPlain((user))
    user.update_location(540, 530)
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
        #sprites.update()
        #only needed to be call when in combat
        user.movement()

        screen.blit(background, (0, 0))
        sprites.draw(screen)
        pygame.display.update()

        

    
        
if __name__ == "__main__":
    main()
        