from itertools import count
from polytanks.engine import AbstractEngine

class Engine(AbstractEngine):
    def __init__(self, pools, start_id):
        super().__init__(pools, start_id)
        self.regenerate_id()

    def update(self, dt):
        pass

    def generate_id(self):
        return next(self.id_generator)

    def regenerate_id(self):
        self.id_generator = count(self.start_id)
