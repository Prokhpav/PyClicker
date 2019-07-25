import Constants
import math

#   name_from:  # func view
functions = {
    'line_u': lambda x: 1 - x,                           # \
    'line_d': lambda x: x,                               # /
    'circle_uu': lambda x: (1 - x ** 2) ** 0.5,          # ^\
    'circle_du': lambda x: (2 * x - x ** 2) ** 0.5,      # /^
    'circle_ud': lambda x: 1 - (2 * x - x ** 2) ** 0.5,  # \_
    'circle_dd': lambda x: 1 - (1 - x ** 2) ** 0.5,      # _/
    'sinus_u': lambda x: math.sin(x * 2 * math.pi),      # ^v
    'sinus_d': lambda x: -math.sin(x * 2 * math.pi)      # v^
}


class Action:
    def __init__(self, arg, func_name, time, work, end_func=None):
        self.t = 0
        self.action_arg = arg
        self.first_value = None
        self.func = functions[func_name]
        self.time = time
        self.work = work
        self.end_func = end_func

    def update(self, obj):
        if self.t == 0:
            self.first_value = obj.__dict__[self.action_arg]
        self.t = min(self.time, self.t + Constants.runspeed)
        if self.t <= self.time:
            obj.__setattr__(self.action_arg, self.first_value + self.work * self.func(self.t / self.time))
            if self.t == self.time:
                if self.end_func is not None:
                    self.end_func(obj)
                obj.actions.remove(self)
