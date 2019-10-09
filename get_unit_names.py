import os


resource_directory = "resources"

unit_names = "Monk · Villager · Trade Cart · Trade Cog · Fishing Ship · Transport Ship Infantry	Militia · Man-at-Arms · Long Swordsman · Two-Handed Swordsman · Champion Spearman · Pikeman Archers	Archer · Crossbowman · Arbalest Skirmisher · Elite Skirmisher Hand Cannoneer Cavalry Archer · Heavy Cavalry Archer Cavalry	Scout Cavalry · Light Cavalry Knight · Cavalier · Paladin Camel · Heavy Camel Siege	Battering Ram · Capped Ram · Siege Ram Scorpion · Heavy Scorpion Bombard Cannon Trebuchet Navy	Galley · War Galley · Galleon Fire Ship · Fast Fire Ship Demolition Ship · Heavy Demolition Ship Cannon Galleon · Elite Cannon Galleon Unique	Longbowman · Cataphract · Woad Raider · Chu Ko Nu · Throwing Axeman · Huskarl · Samurai · War Elephant · Mameluke · Teutonic Knight · Janissary · Berserk · Mangudai  · Longboat ConquerorsIcon The Conquerors Hussar · Petard · War Wagon · Turtle Ship · Halberdier · Eagle Warrior · Elite Eagle Warrior · Jaguar Warrior · Tarkan · Missionary · Conquistador · Plumed Archer ForgottenIcon The Forgotten Imperial Camel · Eagle Scout  · Slinger · Genoese Crossbowman · Condottiero · Elephant Archer · Kamayuk · Magyar Huszar · Boyar AfricanIcon The African Kingdoms Fire Galley  · Demolition Raft · Camel Archer · Genitour · Gbeto · Shotel Warrior  · Caravel  · Organ Gun  · Siege Tower RajaIcon Rise of the Rajas Imperial Skirmisher  · Battle Elephant · Elite Battle Elephant · Arambai · Ballista Elephant · Karambit Warrior · Rattan Archer".split("·")
unit_names += ['Castle', 'Watch Tower (Age of Empires II)']
with open(os.path.join(resource_directory, "units.txt"), 'w') as f:
    for unit in unit_names:
        f.write(unit.strip())
        f.write("\n")