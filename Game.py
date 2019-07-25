import pygame
from AllGlobals import *
import Constants


class GameClass(Node):
    def __init__(self):
        super().__init__(size=Constants.SCREEN_SIZE, touching=True)
        self.parent = Globals.screen
        self.running = False
        self.touch_pos = [False, False, False]
        self.key_keeping = set()
        self.setup()

    def setup(self):
        pass

    def run(self):
        self.running = True
        while self.running:
            self._check_events()
            self._update()
            self._draw()
            pygame.display.update()
            Globals.timer.tick(Constants.fps)

    def _check_events(self):
        events = {}
        for event in pygame.event.get():
            if event.type in events.keys():
                events[event.type].append(event)
            else:
                events[event.type] = [event]

        if pygame.QUIT in events.keys():
            self.running = False

        if pygame.KEYDOWN in events.keys():
            for event in events.pop(pygame.KEYDOWN):
                key = event.key
                self.key_keeping.add(key)
                self.key_down(key)

        elif pygame.KEYUP in events.keys():
            for event in events.pop(pygame.KEYUP):
                key = event.key
                self.key_keeping.remove(key)
                self.key_up(key)

        if pygame.MOUSEBUTTONDOWN in events.keys():
            self.touch_pos = [False, False, False]
            for event in events.pop(pygame.MOUSEBUTTONDOWN):
                if event.button <= 3:
                    self.touch_pos[event.button - 1] = Point(event.pos)
                self._touch_began(Point(event.pos), event.button)

        if pygame.MOUSEBUTTONUP in events.keys():
            for event in events.pop(pygame.MOUSEBUTTONUP):
                if event.button <= 3:
                    self.touch_pos[event.button - 1] = False
                self._touch_ended(Point(event.pos), event.button)

        if pygame.MOUSEMOTION in events.keys():
            event = events[pygame.MOUSEMOTION][0]
            if self.touch_pos.count(False) != 3:
                buttons = [0 if i is False else 1 for i in self.touch_pos]
                for pos in self.touch_pos:
                    if pos is not False:
                        self._touch_dragging(pos, Point(event.pos), Point(event.rel), buttons)
            else:
                self._touch_moving(Point(event.pos), Point(event.rel))
        self.check_events(events)

    def check_events(self, events: dict):
        pass

    def key_down(self, key):
        pass

    def key_up(self, key):
        pass

    def update(self):
        pass


class Game(GameClass):
    def setup(self):
        self.bcolor = (0, 0, 0)
        self.drag_plate = DragPlate(Settings.drag_plate_tile, Globals.miners_images, Settings.drag_plate_pos,
                                    Settings.drag_plate_size, bcolor=Settings.drag_plate_bcolor, parent=self)
        self.cave_screen = CaveNode(50, (188, 124, 61), pos=(Settings.drag_plate_size[0], 0),
                                    size=(Constants.SCREEN_SIZE[0] - Settings.drag_plate_size[0],
                                          Constants.SCREEN_SIZE[1]), bcolor=(0, 0, 0), parent=None)
        self.cave_screen.segments.append(Point(self.cave_screen.size) / (2, 2))
        self.cave_screen.segments.append(Point(0, 0))
        self.move_value = Point(100 * Constants.runspeed, 0)

        self.dot_test = MyDot(pygame.transform.scale(pygame.image.load('Sprites/circle.png'), (300, 300)), (0, 0),
                              pos=(Settings.drag_plate_size[0] + 300, 300),
                              size=(Constants.SCREEN_SIZE[0] - Settings.drag_plate_size[0],
                                    Constants.SCREEN_SIZE[1]), bcolor=(0, 0, 0), parent=self, zpos=-1)

    def key_down(self, key):
        if key in (273, 274):
            a = True
            if key == 273:  # and self.move_value.y != self.move_value.x - 0.1:
                # self.move_value.y = min(self.move_value.x - 0.1, self.move_value.y + 20 * Constants.runspeed)
                self.dot_test.change_rotate(self.dot_test.dot_rotate + 5)
            elif key == 274:  # and self.move_value.y != 0.1 - self.move_value.x:
                # self.move_value.y = max(0.1 - self.move_value.x, self.move_value.y - 20 * Constants.runspeed)
                self.dot_test.change_rotate(self.dot_test.dot_rotate - 5)
            else:
                a = False
            if a:
                pass
                # self.cave_screen.segments.append(Point(0, 0))

    # def key_up(self, key):
    #     if key in (273, 274):
    #         self.cave_screen.segments.append(Point(0, 0))

    def update(self):
        pass
        # self.cave_screen.move(self.move_value)
        # self.cave_screen.segments[-1] = Point(self.cave_screen.size) / (2, 2)


Game().run()
pygame.quit()
