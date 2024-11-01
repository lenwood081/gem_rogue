from drops.Items.Item import Item
from sprites.weapons.Guns.PlasmaGun import PlasmaGun 
from Actions.WeaponFire import WeaponFire 
from config import SCALE_FACOTOR
import pygame

class PlasmaGunItem(Item): 
    def __init__(self, id):
        super().__init__("Plasma Gun", "Active", id)
        self.icon = pygame.transform.scale(pygame.image.load("assets/weapons/PlasmaGun1.png").convert_alpha(), (28*8, 16*8))
        self.description = "More damage and projectile speed, shoot slightly slower though."

    # added item to item list, add item to actions list
    def connect(self, parent):
        super().connect(parent)
        
        parent.actions.append(WeaponFire(1, "Plasma Gun", parent, PlasmaGun))
        parent.determine_angles()

    # for when an item is removed
    def remove(self):
        pass