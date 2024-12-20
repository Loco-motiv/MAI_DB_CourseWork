from enum import Enum

class WeaponTypes(Enum):
    AutoRifle = 6
    Shotgun = 7
    MachineGun = 8
    HandCannon = 9
    RocketLauncher = 10
    FusionRifle = 11
    SniperRifle = 12
    PulseRifle = 13
    ScoutRifle = 14
    Sidearm = 17
    Sword = 18
    LinearFusionRifle = 22
    GrenadeLauncher = 23
    SubmachineGun = 24
    TraceRifle = 25
    Bow = 31
    Glaive = 33

class Elements(Enum):
    Kinetic = 1
    Arc = 2
    Solar = 3
    Void = 4
    Stasis = 6
    Strand = 7

class Rarity(Enum):
    Common = 2
    Uncommon = 3
    Rare = 4
    Legendary = 5
    Exotic = 6

class ArmorTypes(Enum):
    HelmetArmor = 26
    GauntletsArmor = 27
    ChestArmor = 28
    LegArmor = 29
    ClassArmor = 30

class Classes(Enum):
    Titan = 0
    Hunter = 1
    Warlock = 2

class Roles(Enum):
    User = 0
    Moderator = 1
    Administrator = 2