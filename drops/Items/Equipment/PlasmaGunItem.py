from drops.Items.Item import Item
from sprites.weapons.Guns.PlasmaGun import PlasmaGun 

class PlasmaGunItem(Item): 
    def __init__(self):
        super().__init__("Plasma Gun", "Weapon")