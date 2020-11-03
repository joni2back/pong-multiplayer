import pyglet

class SprObj(pyglet.sprite.Sprite):

    img = None

    def __init__(self, img, x=0, y=0, blend_src=770, blend_dest=771, batch=None, group=None, usage='dynamic'):
        pyglet.sprite.Sprite.__init__(self, img, x, y, blend_src, blend_dest, batch, group, usage)
        self.img = img

    @property
    def left(self):
        return self.x

    @property
    def right(self):
        return self.x + self.width

    @property
    def top(self):
        return self.y + self.height

    @property
    def bottom(self):
        return self.y

    # bounds: (min, max)
    def move(self, dx, dy, x_bounds=None, y_bounds=None):
        return self.move_absolute(self.x + dx, self.y + dy, x_bounds=x_bounds, y_bounds=y_bounds)

    # bounds: (min, max)
    def move_absolute(self, x, y, x_bounds=None, y_bounds=None):
        if x_bounds is not None:
            x = min(max(x, x_bounds[0]), x_bounds[1])
        if y_bounds is not None:
            y = min(max(y, y_bounds[0]), y_bounds[1])
        self.update(x=x, y=y)

    def set_width(self, width):
        self.img.width = width

    def set_height(self, height):
        self.img.height = height

    def center_anchor_y(self, window_height):
        self.y = window_height / 2 - self.height // 2
        return self

    def center_anchor_x(self, window_width):
        self.x = window_width / 2 - self.width // 2
        return self

    def check_collision(self, others_list):
        for sprite in others_list:
            if (self.bottom <= sprite.top and self.top >= sprite.bottom and
                self.right >= sprite.left and self.left <= sprite.right):
                print(f"Object collision: {self.position} with {sprite.position}")
                return sprite

    def check_collision_laterals(self, window_height):
        if self.top > window_height or self.top < self.height:
            print(f"Lateral collision: {self.position} with window")
            return True
