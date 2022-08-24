import pygame as pg
import settings as st

class Bullet(pg.sprite.Sprite):
    def __init__(self, position, surface, dir, groups):
        super().__init__(groups)

        self.z = st.LAYERS['Level']

        self.image = surface
        # Make the bullet point in direction of shot.
        if(dir.x < 0):
            self.image = pg.transform.flip(self.image, True, False)
        
        self.rect = self.image.get_rect(center=position)

        # Float based movement.
        self.direction = dir
        self.speed = 500
        self.pos = pg.math.Vector2(self.rect.center)

        self.start_time = pg.time.get_ticks()

    def update(self, deltaTime):
        self.pos += self.direction*self.speed*deltaTime
        self.rect.center = (round(self.pos.x), round(self.pos.y))

        # Destroy bullets after a certain time to improve performance.
        if(pg.time.get_ticks() - self.start_time > 1500):  # 1.5 seconds.
            self.kill()
