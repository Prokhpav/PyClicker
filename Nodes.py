import pygame
from Actions import Action as A
from Settings import Settings, Text
import math
from images import *
from typing import Dict, Set


class Node(pygame.Surface):
    def __init__(self, pos=(0, 0), size=(0, 0), zpos=0, anchor_point=(0, 0), bcolor=None, touching=False, parent=None,
                 **kwargs):
        self._arg = 'size'
        super().__init__(size, **kwargs)
        self.children: Dict[int, Set[Node]] = {}

        a = self.children.values()
        self.texts: {Text} = set()
        self.actions = set()
        self.zpos = zpos
        self.size = list(size)
        self.anchor_point = anchor_point
        self.pos = Point(pos)
        self.pos = list(self.pos - Point(anchor_point) * self.size)
        self.bcolor = bcolor
        self.touching = touching
        self.image = False
        self.parent = parent
        if parent is not None:
            self.parent.add_child(self)

    def __contains__(self, item: Point or list):
        if isinstance(item, Point):
            return (0, 0) <= item <= self.size
        return 0 <= item[0] <= self.size[0] and 0 <= item[1] <= self.size[1]

    def add_child(self, child):
        if isinstance(child, Node):
            child.parent = self
            if child.zpos in self.children.keys():
                self.children[child.zpos].add(child)
            else:
                self.children[child.zpos] = {child}
        elif isinstance(child, Text):
            self.texts.add(child)

    def del_child(self, child):
        if isinstance(child, Node):
            child.parent = None
            if len(self.children[child.zpos]) > 1:
                self.children[child.zpos].remove(child)
            else:
                self.children.pop(child.zpos)
        elif isinstance(child, Text):
            self.texts.remove(child)

    def func_to_children(self, func, *args):
        for zpos in reversed(sorted(self.children.keys())):
            for child in self.children[zpos]:
                func(child)

    def _update(self):
        if self.actions:
            for action in self.actions.copy():
                action.update(self)
        self.func_to_children(lambda child: child._update())
        self.update()

    def _draw(self):
        if self.bcolor is not None:
            self.fill(self.bcolor)
        if self.image is not False:
            self.blit(self.image, (0, 0))
        self.func_to_children(lambda child: child._draw())
        if self.texts:
            for t in self.texts:
                self.blit(t.image, t.image_rect)
        self.draw()
        if self.parent is not None:
            self.parent.blit(self, self.pos)

    def update(self):
        pass

    def draw(self):
        pass

    def _touch_began(self, touch: Point, button):
        if self.touching:
            pos = touch - self.pos
            if (0, 0) <= pos <= self.size:
                self.touch_began(pos, button)
                self.func_to_children(lambda child: child._touch_began(pos, button), pos, button, '!!!!!', '3')

    def touch_began(self, touch: Point, button):
        pass

    def _touch_ended(self, touch: Point, button):
        if self.touching:
            pos = touch - self.pos
            self.touch_ended(touch, button)
            self.func_to_children(lambda child: child._touch_ended(pos, button))

    def touch_ended(self, touch: Point, button):
        pass

    def _touch_dragging(self, first_pos: Point, new_pos: Point, rel: Point, buttons):
        if self.touching:
            first_pos, new_pos = first_pos - self.pos, new_pos - self.pos
            if (0, 0) <= first_pos <= self.size or (0, 0) <= new_pos - rel <= self.size:
                self.touch_dragging(first_pos, new_pos, rel, buttons)
                self.func_to_children(lambda child: child._touch_dragging(first_pos, new_pos, rel, buttons))

    def touch_dragging(self, first_pos: Point, new_pos: Point, pred_pos: Point, buttons):
        pass

    def _touch_moving(self, new_pos: Point, rel: Point):
        new_pos = new_pos - self.pos
        if (0, 0) <= new_pos - rel <= self.size:
            self.touch_moving(new_pos, rel)
            self.func_to_children(lambda child: child._touch_moving(new_pos, rel))

    def touch_moving(self, new_pos: Point, pred_pos: Point):
        pass

    def __str__(self):
        return self.__class__.__name__ + '(%s: %r)' % (self._arg, self.__dict__[self._arg])

    def __repr__(self):
        return self.__str__()


class DragPlate(Node):
    def __init__(self, tile_size, draw_list: list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._arg = 'drag_value'
        for child in draw_list:
            child.pos[1] = -tile_size
            self.add_child(child)
        self.touching = True
        self.touched = False
        self.imin = 0
        self.imax = 0
        self.pmin = 0
        self.draw_list = draw_list
        self.drag_value = 0
        self.first_drag = None
        self.drag_speed = 0
        self.tile_size = tile_size

    def __setattr__(self, key, value):
        # if key == 'drag_value' and hasattr(self, 'tile_size'):
        #     m = len(self.draw_list) * self.tile_size
        #     if value > m - self.size[1]:
        #         if value > m:
        #             value = m
        #         if not self.touched and not self.actions:
        #             self.actions.add(A('drag_value', 'circle_du', 1, -(self.size[1] + value - m)))
        #     elif value < 0:
        #         if value < -self.size[1]:
        #             value = -self.size[1]
        #         if not self.touched and not self.actions:
        #             self.actions.add(A('drag_value', 'circle_du', 1, -value))
        super().__setattr__(key, value)
        if key in ('drag_value', 'tile_size') and hasattr(self, 'tile_size'):
            self.imin = max(0, int(self.drag_value / self.tile_size))
            self.imax = min(int((self.drag_value + self.size[1]) / self.tile_size), len(self.draw_list) - 1)
            self.pmin = -(self.drag_value % self.tile_size) if self.drag_value >= 0 else -self.drag_value

    def _draw(self):
        if self.bcolor is not None:
            self.fill(self.bcolor)
        if self.image is not False:
            self.blit(self.image, (0, 0))
        pos = self.pmin
        for tile in self.draw_list[self.imin:self.imax + 1]:
            tile.pos[1] = Settings.drag_button_pos[1] + pos
            tile._update()
            tile._draw()
            pos += self.tile_size
        if self.parent is not None:
            self.parent.blit(self, self.pos)

    def _touch_began(self, touch: Point, button):
        super()._touch_began(touch, button)

    def touch_began(self, touch: Point, button):
        if button == 1:
            self.touched = True
            self.first_drag = self.drag_value
            if self.actions:
                self.actions.clear()

    def touch_ended(self, touch: Point, button):
        if self.touched:
            self.touched = False
            m = self.drag_value + self.size[1] - self.tile_size * len(self.draw_list)
            if m > 0:
                self.actions.add(A('drag_value', 'circle_du', m / self.size[1], -m))
            elif self.drag_value < 0:
                self.actions.add(A('drag_value', 'circle_du', -self.drag_value / self.size[1], -self.drag_value))
            else:
                pass

    def touch_dragging(self, first_pos: Point, new_pos: Point, rel: Point, buttons):
        if buttons[0] and self.touched:
            self.drag_value = min(max(self.first_drag + (first_pos.y - new_pos.y), -self.size[1]),
                                  self.tile_size * len(self.draw_list))
            self.drag_speed = rel.y


class SpriteNode(Node):
    def __init__(self, image, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._arg = 'image'
        self.image = pygame.transform.scale(pygame.image.load(image), self.size) if isinstance(image, str) else image


class TextNode(Node):
    def __init__(self, text, font: pygame.font.Font, color=(0, 0, 0), *args, **kwargs):
        self.text = text
        self.font = font
        self.text_color = color
        self.image = None
        size = self.image.get_rect().size
        super().__init__(*args, **kwargs, size=size)
        # self.set_alpha(128)
        self._arg = 'text'

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        if key in ('text', 'font', 'text_color', 'image') and hasattr(self, 'image'):
            self.__dict__['image'] = self.font.render(self.text, True, self.text_color)


class ButtonNode(Node):
    def __init__(self, textures, touch_func, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.touching = True
        self.touch_func = touch_func
        self.focused, self.touched = False, False
        #                       (focused, touched)
        self.textures = dict(zip(((False, False), (True, False), (True, True), (False, True)), textures))
        self.image = self.textures[(False, False)]

    def __setattr__(self, key, value):
        if key in ('focused', 'touched') and hasattr(self, 'textures') and value != self.__dict__[key]:
            self.__dict__[key] = value
            self.image = self.textures[(self.focused, self.touched)]
        else:
            super().__setattr__(key, value)

    def touch_moving(self, new_pos: Point, pred_pos: Point):
        self.focused = (new_pos in self)

    def touch_began(self, touch: Point, button):
        if button == 1:
            self.touched = True

    def touch_ended(self, touch: Point, button):
        if button == 1 and self.touched:
            self.touched = False
            if self.focused:
                self.touch_func(self)

    def touch_dragging(self, first_pos: Point, new_pos: Point, pred_pos: Point, buttons):
        self.focused = (new_pos in self)


class ButtonImage(Node):
    def __init__(self, image, pos, size, name, cost, factor, *args, **kwargs):
        super().__init__(pos, size, *args, **kwargs)
        self.touching = True
        self.image = image
        self.buy_text_image = Settings.buy_text_image.copy()
        self.add_child(self.buy_text_image)
        self.name_image = Text('', Settings.text_font, self)
        self.name = name
        self.level_image = Text('', Settings.text_font, None)
        self.level = 0
        self.name_image.image_rect.topleft = Settings.text_name_pos
        self.cost_image = Text('', Settings.text_font, self)
        self.cost = cost
        self.factor_image = Text('', Settings.text_font, None)
        self.factor = Long(0)
        self.f_per_level = factor
        self.button_image = ButtonNode(Settings.buy_button_images, self.buttontouch, pos=Settings.buy_button_pos,
                                       size=Settings.buy_button_size, parent=self)

    def __setattr__(self, key, value):
        if key == 'name':
            self.name_image.text = str(value)
            self.name_image.image_rect.topleft = Settings.text_name_pos
        elif key == 'level':
            self.level_image.text = Settings.level_text + str(value)
            self.level_image.image_rect.topleft = Settings.text_level_pos
            if hasattr(self, 'level') and self.level == 0:
                self.buy_text_image.text = Settings.upgrade_text
                self.buy_text_image.image_rect.center = Settings.buy_text_pos
                self.add_child(self.level_image)
                self.add_child(self.factor_image)
        elif key == 'cost':
            self.cost_image.text = str(value)
            self.cost_image.image_rect.center = Settings.text_cost_pos
        elif key == 'factor':
            self.factor_image.text = str(value)
            self.factor_image.image_rect.center = Settings.text_factor_pos
        super().__setattr__(key, value)

    def buttontouch(self, button):
        self.cost *= 1.5
        self.level += 1
        if self.level >= 200 and self.level % 25 == 0:
            self.f_per_level *= 4
            self.factor *= 4
        self.factor += self.f_per_level


class CaveNode(Node):
    def __init__(self, segment_size, color=(0, 0, 0), *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.touching = True
        self.segments: list = []
        self.segment_size = segment_size
        self.segment_color = color

    def _draw(self):
        if self.bcolor is not None:
            self.fill(self.bcolor)
        if self.image is not False:
            self.blit(self.image, (0, 0))
        if len(self.segments) >= 2:
            pygame.draw.lines(self, self.segment_color, False, list(map(list, self.segments)), self.segment_size)
        self.func_to_children(lambda child: child._draw())
        if self.parent is not None:
            self.parent.blit(self, self.pos)
        self.draw()

    def move(self, value):
        for pos in self.segments:
            pos -= value
        i = 1
        for i in range(1, len(self.segments)):
            if self.segments[i].x > 0:
                break
        if i > 1:
            self.segments = self.segments[i - 1:]

    def touch_began(self, touch: Point, button):
        if button == 1:
            self.segments.append(touch)
        elif button == 2:
            self.move(20)
        elif button == 3 and self.segments:
            self.segments = self.segments[1:]

    def touch_dragging(self, first_pos: Point, new_pos: Point, pred_pos: Point, buttons):
        if buttons[0] and new_pos in self:
            self.segments[-1] = new_pos


class MyDot(Node):
    def __init__(self, image: pygame.Surface, dot_pos, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bcolor = (10, 10, 10)
        self.image_ = image
        self.img_size = image.get_size()
        self.true_pos = self.pos
        self.rot_image = image
        self.dot_true_pos = dot_pos
        self.dot_pos = dot_pos
        self.dot_ways = [i - j for i, j in zip(Point(self.size) / (2, 2), dot_pos)]
        self.dot_ways.append((self.dot_ways[0] ** 2 + self.dot_ways[1] ** 2) ** 0.5)
        #    dot_ways = [a, b, c] sin(r) = a/c, cos(r) = b/c, tg(r) = a/b
        self.dot_true_rotate = math.asin(self.dot_ways[0] / self.dot_ways[2])
        self.dot_rotate = self.dot_true_rotate
        self.change_rotate(0)

    def change_rotate(self, new_rotate):
        self.rot_image = pygame.transform.rotate(self.image_, new_rotate)
        self.img_size = self.rot_image.get_size()
        self.dot_rotate = new_rotate
        d = self.dot_true_rotate + math.radians(self.dot_rotate)  # поворот точки относительно центра
        self.dot_pos = [int(self.dot_ways[2] * math.sin(d)), int(self.dot_ways[2] * math.cos(d))]
        self.dot_pos = [int(self.img_size[i] / 2) for i in range(2)]
        self.pos = [self.true_pos[i] - self.dot_pos[i] for i in range(2)]

    def draw(self):
        self.blit(self.rot_image, (0, 0))
        pygame.draw.circle(self, (255, 0, 0), self.dot_pos, 10)
