class AbstractEngine:
    def __init__(self, pools):
        types = ("player",)
        for t in types:
            if t not in pools:
                raise Exception("{} not found in pools".format(t))
        self.pools = pools
        self.entities = {}
    
    def regenerate_id(self):
        raise NotImplementedError

    def add_player(self, id=None):
        player_pool = self.pools.get("player")
        player = player_pool()
        if player is None:
            return 
        id = id if isinstance(id, int) else self.generate_id()
        self.entities[id] = player
        return (id, player)

    def remove(self, id):
        entity = self.entities.get(id)
        if not entity:
            return False
        entity.free()
        del self.entities[id]
        return True

    def update(self, dt):
        raise NotImplementedError

    def generate_id(self):
        raise NotImplementedError
