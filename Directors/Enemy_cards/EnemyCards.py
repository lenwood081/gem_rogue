from Directors.Card import Card
from sprites.enemies.BlockRanged import BlockRanged
from sprites.enemies.BlockFodder import BlockFodder

# list of all enemy cards
ENEMYCARDS = [
    Card("Block Fodder", BlockFodder, "Basic Enemy", 14, 1),
    Card("Block Ranged", BlockRanged, "Basic Enemy", 10, 1),
]