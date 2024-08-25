

class Enemy_controller:
    def __init__(self, spend):
        self._max_spend = spend
        
    def spawn_enemy(self):
        # retrun refernec to new enemy
        return