from drops.Items.Item import Item
from sprites.weapons.Guns.PlasmaGun import PlasmaGun 
from Actions.WeaponFire import WeaponFire 

class PlasmaGunItem(Item): 
    def __init__(self, id):
        super().__init__("Plasma Gun", "Weapon", id)

    # added item to item list, add item to actions list
    def connect(self, parent):
        parent.actions.append(WeaponFire(1, "Plasma Gun", self, PlasmaGun, math.pi/8))
        pass

    # for when an item is removed
    def remove(self):
        pass