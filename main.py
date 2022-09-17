import pygame, random
pygame.init()
# initialization
SCREENSIZE = 1800, 950
SCREEN = pygame.display.set_mode(SCREENSIZE)
ICON = pygame.image.load(__file__[:-7] + 'Assets\\icon.png')
pygame.display.set_caption('Bitmon V2')
pygame.display.set_icon(ICON)

gameSave = eval(open(__file__[:-7] + 'data\\GameSave.txt').read())
print(gameSave)

class texturesClass:
    def __init__(self):
        self.grass = pygame.image.load(__file__[:-7] + 'Assets\\grass.png')
        self.playerWalk = pygame.image.load(__file__[:-7] + 'Assets\\CharacterSprite.png')
        self.homebg = pygame.image.load(__file__[:-7] + 'Assets\\homeBackdrop.png')
        self.rock = pygame.image.load(__file__[:-7] + 'Assets\\rock.png')
        self.dungeonbg = pygame.image.load(__file__[:-7] + 'Assets\\dungeonBG1.png')
        self.portalSpriteSheet = pygame.image.load(__file__[:-7] + 'Assets\\portal.png')
        self.regularDoor = pygame.image.load(__file__[:-7] + 'Assets\\door.png')
        self.arrow = pygame.image.load(__file__[:-7] + 'Assets\\Arrow.png')
        self.male = pygame.image.load(__file__[:-7] + 'Assets\\MaleSymbol.png')
        self.female = pygame.image.load(__file__[:-7] + 'Assets\\FemaleSymbol.png')
        self.portalFrame = 0
        self.portal = self.portalSpriteSheet.subsurface(((self.portalFrame//15)*32, 0, 32, 32))

    def frameUpdate(self):
        self.portalFrame += 1
        if self.portalFrame >= 60:
            self.portalFrame = 0
        self.portal = self.portalSpriteSheet.subsurface(((self.portalFrame//15)*32, 0, 32, 32))

    def resize(self, texture, size):
        return pygame.transform.scale(texture, size)
textures = texturesClass()

class player:
    def __init__(self, animation, x, y):
        self.x = x
        self.y = y
        self.animation = animation
        self.dir = 0
        self.frame = self.animation.subsurface((0,32*[3,2,0,1][self.dir],32,32))
        self.sprinting = False
        self.allBitmon = []
        self.bitmonTeam = None
    
    def addBitmon(self, bitmonObj):
        self.allBitmon.append(bitmonObj)

    def move(self, direction):
        global room 
        directions = ((0,-1), (1,0), (0,1), (-1,0))
        self.dir = direction
        if (self.x + directions[direction][0] not in range(19) or self.y + directions[direction][1] not in [i for i in range(9)]):
            self.frame = self.animation.subsurface((0,32*[3,2,0,1][self.dir],32,32))
            return
        elif room[int(self.x) + directions[direction][0]][int(self.y) + directions[direction][1]] == 2: 
            self.frame = self.animation.subsurface((0,32*[3,2,0,1][self.dir],32,32))
            return
        for i in range(16):
            self.x += directions[direction][0]*(1/16)
            self.y += directions[direction][1]*(1/16)
            self.frame = self.animation.subsurface((32*(i//4),32*[3,2,0,1][self.dir],32,32))
            draw()
            textures.frameUpdate()
            if not self.sprinting: textures.frameUpdate()
            clock.tick(72 if self.sprinting else 36)
        self.frame = self.animation.subsurface((0,32*[3,2,0,1][self.dir],32,32))

class BitmonClass:
    def __init__(self, name, level, exp, type, health, attack, defence, speed, manaMax, manaFill, Hup, Aup, Dup, Sup, MMup, MFup, color, evolvl, moveList, moveLearnList, gender, animation):
        self.name = name
        self.level = level
        self.exp = exp
        self.type = type
        self.health = health
        self.attack = attack
        self.defence = defence
        self.speed = speed
        self.manaMax = manaMax
        self.manaFill = manaFill
        self.Hup = Hup
        self.Aup = Aup
        self.Dup = Dup
        self.Sup = Sup
        self.MMup = MMup
        self.MFup = MFup
        self.color = color
        self.evolvl = evolvl
        self.moveList = moveList
        self.moveLearnList = moveLearnList
        self.gender = gender
        self.animation = animation
    
    def levelUp(self, levels=1):
        self.level += levels
        for _ in range(levels):
            self.health += self.Hup
            self.attack += self.Aup
            self.defence += self.Dup
            self.speed += self.Sup
            self.manaMax += self.MMup
            self.manaFill += round(self.MFup/3,2)
        return self

    def expToLevel(self):
        return (self.level**2.08)+10

def setupmoves():
    #name,dmg,engergy cost,type   
    #  ,['',,,0],
    return [
        [ #Basic moves  (must have 1)
        [['Burn',9,13,0],['Fireflies',5,8,0],['Fire Dash',14,20,0],['Searing Skratch',12,18,0],['Bonfire',10,15,0],['Flare',7,10,0]],#fire
        [['Mist',3,5,1],['Water Bomb',13,19,1],['Snow Slice',11,16,1],['Ice Peck',7,10,1],['Freezing wind',8,12,1],['Ice Shower',14,20,1]],#water
        [['Absorb',8,13,2],['Pollen Shot',4,7,2],['Root Grasp',7,12,2],['Mossy Touch',5,8,2],['Seed Shot',13,19,2],['Tumble Weed',10,15,2]],#earth
        [['Talon',6,10,3],['Swoop',9,14,3],['Fly',10,14,3],['Peck',11,16,3],['Cloud Cover',14,20,3],['Gust',8,13,3]],#air
        [['Zap',6,9,4],['Spark',8,13,4],['Shocking Grasp',11,16,4],['Energy Shot',10,14,4],['Electrify',13,19,4],['Short Circuit',12,17,4]],#electric
        [['Bite',5,7,5],['Dark Grasp',8,12,5],['Ghost Slice',6,9,5],['Spirit Talons',12,17,5],['Nightfall',15,23,5],['Blacken',10,16,5]],#dark
        [['Scratch',9,13,6],['Stab',6,10,6],['Slice',10,15,6],['Punch',15,22,6],['Slash',11,17,6],['Kick',12,18,6],['Tackle',7,11,6],['Dash',8,13,6]],#normal
        ],
        [ #normal moves (must have 2) 15-35 dmg   22-45 eng   3xlow  5xmid  3x high
        [['Magma Shot',16,24,0],['Heat Wave',19,28,0],['Molten Peck',21,32,0],['Flame Wheel',23,36,0],['Burning Talons',24,36,0],['Fireball',25,37,0],['Firefang',26,38,0],['Flame Breath',27,41,0],['Flame Geyser',30,47,0],['Lava Pool',31,46,0],['Explotion',32,49,0]],#fire
        [['Whirlpool',16,25,1],['Water Jet',19,29,1],['Water Jaws',20,31,1],['Ice Shot',22,32,1],['Icy Wave',23,36,1],['Frost Blast',26,39,1],['Tidal Punch',27,41,1],['Icicle',28,41,1],['Frost Geyser',29,45,1],['Hail Shards',30,45,1],['Frostbite',31,47,1]],#water
        [['Grass Blade',24,36,2],['Earth Punch',22,32,2],['Vine Trap',17,26,2],['Living Fangs',25,37,2],['Grass Bomb',18,28,2],['Thorn Whip',29,44,2],['Splinter',21,32,2],['Bolder Barrage',28,42,2],['Poison Sting',28,43,2],['Thorn Blast',26,40,2],['Leaf Storm',28,41,2],['Rotting Spell',29,42,2]],#plant
        [['Slashing Breeze',25,38,3],['Wing Slice',19,29,3],['Sky Punch',23,35,3],['Air Cutters',26,40,3],['Sky Dash',24,37,3],['Wind Slash',27,39,3],['Sky Dance',17,25,3],['Cloud Crash',29,43,3],['Wind Blast',15,21,3],['Fatal Storm',33,47,3],['Air Blade',20,31,3]],#air
        [['Lightning Bolt',24,36,4],['Energy Fang',21,32,4],['Wire Slice',22,34,4],['Power Punch',18,27,4],['Wire Whip',20,31,4],['Lighting Dash',22,34,4],['Superfang',30,44,4],['Lightning Burst',28,42,4],['Thunder Punch',27,40,4],['Thunder Beam',26,39,4],['Volt Pulse',29,43,4]],#electric
        [['Dark Punch',18,27,5],['Night Slash',27,41,5],['Ghost Blast',20,30,5],['Dark Blade',26,40,5],['Shadow Punch',21,32,5],['Black Fangs',31,47,5],['Night Jaws',23,35,5],['Dusk Pulse',26,38,5],['Spirit Fangs',24,38,5],['Shadow Slash',28,41,5],['Hex Burst',29,42,5]],#dark
        ],
        [ #super moves (50%)  35-55 dmg   55-85 eng   low,mid,mid,high
        [['Meteor',43,65,0],['Nova Burst',51,77,0],['Solar Ray',46,68,0],['Erruption',39,58,0]],#fire
        [['Tsunami',53,80,1],['Downfall',36,56,1],['Piercing Rain',47,70,1],['Waterfall',42,63,1]],#water
        [['Earth Jaws',45,67,2],['Poison Fang',48,73,2],['Nature Blast',38,57,2],['Fracture',50,72,2]],#earth
        [['Tempest',52,78,3],['Sky Fall',47,71,3],['Tornado',41,61,3],['Hurricane',50,75,3]],#air
        [['Arc Cutter',51,75,4],['Digital Blade',44,66,4],['Megajolt',40,60,4],['Power Surge',35,53,4]],#electric
        [['Nebula',54,82,5],['Spirit Circle',43,64,5],['Shadow Slash',39,58,5],['Black Magic',48,73,5]],#dark
        ],
        [ #recovery (30%)
            ['Rest',0,-10,6],
            ['Nap',2,-17,6], # +5% HP
            ['Sleep',3,-23,6], # +10% HP
            ['Regenerate',4,35,6], #rare +15% HP
            ['Synthesis',10,-20,2], #rare earth only 
            ['Shadow Sleep',15,-16,5], #rare dark only
        ]]
allpkm = [
    'Bulbasaur', 'Ivisaur', 'Venusaur', 'Charmander', 'Charmeleon', 'Charizard', 'Squirtle', 'Wartortle', 'Blastoise', 'Caterpie', 'Metapod', 'Butterfree', 'Weedle', 'Kakuna', 'Beedrill', 'Pidgey', 'Pidgeotto', 'Pidgeot', 'Rattata', 'Raticate', 'Spearow', 'Fearow', 'Ekans', 'Arbok', 'Pikachu', 'Raichu', 'Sandshrew', 'Sandslash', 'Nidoran', 'Nidorina', 'Nidoqueen', 'Nidoran', 'Nidorino', 'Nidoking', 'Clefairy', 'Clefable', 'Vulpix', 'Ninetales', 'Jigglypuff', 'Wigglytuff', 'Zubat', 'Golbat', 'Oddish', 'Gloom', 'Vileplume', 'Paras', 'Parasect', 'Venonat', 'Venomoth', 'Diglett', 'Dugtrio', 'Meowth', 'Persian', 'Psyduck', 'Golduck', 'Mankey', 'Primeape', 'Growlithe', 'Arcanine', 'Poliwag', 'Poliwhirl', 'Poliwrath', 'Abra', 'Kadabra', 'Alakazam', 'Machop', 'Machoke', 'Machamp', 'Bellsprout', 'Weepinbell', 'Victreebel', 'Tentacool', 'Tentacruel', 'Geodude', 'Graveler', 'Golem', 'Ponyta', 'Rapidash', 'Slowpoke', 'Slowbro', 'Magnemite', 'Magneton', 'Farfetched', 'Doduo', 'Dodrio', 'Seel', 'Dewgong', 'Grimer', 'Muk', 'Shellder', 'Cloyster', 'Gastly', 'Haunter', 'Gengar', 'Onix', 'Drowzee', 'Hypno', 'Krabby', 'Kingler', 'Voltorb', 'Electrode', 'Exeggcute', 'Exeggutor', 'Cubone', 'Marowak', 'Hitmonlee', 'Hitmonchan', 'Lickitung', 'Koffing', 'Weezing', 'Rhyhorn', 'Rhydon', 'Chansey', 'Tangela', 'Kangaskhan', 'Horsea', 'Seadra', 'Goldeen', 'Seaking', 'Staryu', 'Starmie', 'Mime', 'Scyther', 'Jynx', 'Electabuzz', 'Magmar', 'Pinsir', 'Tauros', 'Magikarp', 'Gyarados', 'Lapras', 'Ditto', 'Eevee', 'Vaporeon', 'Jolteon', 'Flareon', 'Porygon', 'Omanyte', 'Omastar', 'Kabuto', 'Kabutops', 'Aerodactyl', 'Snorlax', 'Articuno', 'Zapdos', 'Moltres', 'Dratini', 'Dragonair', 'Dragonite', 'Mewtwo', 'Mew', 'Chikorita', 'Bayleef', 'Meganium', 'Cyndaquil', 'Quilava', 'Typhlosion', 'Totodile', 'Croconaw', 'Feraligatr', 'Sentret', 'Furret', 'Hoothoot', 'Noctowl', 'Ledyba', 'Ledian', 'Spinarak', 'Ariados', 'Crobat', 'Chinchou', 'Lanturn', 'Pichu', 'Cleffa', 'Igglybuff', 'Togepi', 'Togetic', 'Natu', 'Xatu', 'Mareep', 'Flaaffy', 'Ampharos', 'Bellossom', 'Marill', 'Azumarill', 'Sudowoodo', 'Politoed', 'Hoppip', 'Skiploom', 'Jumpluff', 'Aipom', 'Sunkern', 'Sunflora', 'Yanma', 'Wooper', 'Quagsire', 'Espeon', 'Umbreon', 'Murkrow', 'Slowking', 'Misdreavus', 'Unown', 'Wobbuffet', 'Girafarig', 'Pineco', 'Forretress', 'Dunsparce', 'Gligar', 'Steelix', 'Snubbull', 'Granbull', 'Qwilfish', 'Scizor', 'Shuckle', 'Heracross', 'Sneasel', 'Teddiursa', 'Ursaring', 'Slugma', 'Magcargo', 'Swinub', 'Piloswine', 'Corsola', 'Remoraid', 'Octillery', 'Delibird', 'Mantine', 'Skarmory', 'Houndour', 'Houndoom', 'Kingdra', 'Phanpy', 'Donphan', 'Porygon2', 'Stantler', 'Smeargle', 'Tyrogue', 'Hitmontop', 'Smoochum', 'Elekid', 'Magby', 'Miltank', 'Blissey', 'Raikou', 'Entei', 'Suicune', 'Larvitar', 'Pupitar', 'Tyranitar', 'Lugia', 'Hooh', 'Celebi', 'Treecko', 'Grovyle', 'Sceptile', 'Torchic', 'Combusken', 'Blaziken', 'Mudkip', 'Marshtomp', 'Swampert', 'Poochyena', 'Mightyena', 'Zigzagoon', 'Linoone', 'Wurmple', 'Silcoon', 'Beautifly', 'Cascoon', 'Dustox', 'Lotad', 'Lombre', 'Ludicolo', 'Seedot', 'Nuzleaf', 'Shiftry', 'Taillow', 'Swellow', 'Wingull', 'Pelipper', 'Ralts', 'Kirlia', 'Gardevoir', 'Surskit', 'Masquerain', 'Shroomish', 'Breloom', 'Slakoth', 'Vigoroth', 'Slaking', 'Nincada', 'Ninjask', 'Shedinja', 'Whismur', 'Loudred', 'Exploud', 'Makuhita', 'Hariyama', 'Azurill', 'Nosepass', 'Skitty', 'Delcatty', 'Sableye', 'Mawile', 'Aron', 'Lairon', 'Aggron', 'Meditite', 'Medicham', 'Electrike', 'Manectric', 'Plusle', 'Minun', 'Volbeat', 'Illumise', 'Roselia', 'Gulpin', 'Swalot', 'Carvanha', 'Sharpedo', 'Wailmer', 'Wailord', 'Numel', 'Camerupt', 'Torkoal', 'Spoink', 'Grumpig', 'Spinda', 'Trapinch', 'Vibrava', 'Flygon', 'Cacnea', 'Cacturne', 'Swablu', 'Altaria', 'Zangoose', 'Seviper', 'Lunatone', 'Solrock', 'Barboach', 'Whiscash', 'Corphish', 'Crawdaunt', 'Baltoy', 'Claydol', 'Lileep', 'Cradily', 'Anorith', 'Armaldo', 'Feebas', 'Milotic', 'Castform', 'Kecleon', 'Shuppet', 'Banette', 'Duskull', 'Dusclops', 'Tropius', 'Chimecho', 'Absol', 'Wynaut', 'Snorunt', 'Glalie', 'Spheal', 'Sealeo', 'Walrein', 'Clamperl', 'Huntail', 'Gorebyss', 'Relicanth', 'Luvdisc', 'Bagon', 'Shelgon', 'Salamence', 'Beldum', 'Metang', 'Metagross', 'Regirock', 'Regice', 'Registeel', 'Latias', 'Latios', 'Kyogre', 'Groudon', 'Rayquaza', 'Jirachi', 'Deoxys', 'Turtwig', 'Grotle', 'Torterra', 'Chimchar', 'Monferno', 'Infernape', 'Piplup', 'Prinplup', 'Empoleon', 'Starly', 'Staravia', 'Staraptor', 'Bidoof', 'Bibarel', 'Kricketot', 'Kricketune', 'Shinx', 'Luxio', 'Luxray', 'Budew', 'Roserade', 'Cranidos', 'Rampardos', 'Shieldon', 'Bastiodon', 'Burmy', 'Wormadam', 'Mothim', 'Combee', 'Vespiquen', 'Pachirisu', 'Buizel', 'Floatzel', 'Cherubi', 'Cherrim', 'Shellos', 'Gastrodon', 'Ambipom', 'Drifloon', 'Drifblim', 'Buneary', 'Lopunny', 'Mismagius', 'Honchkrow', 'Glameow', 'Purugly', 'Chingling', 'Stunky', 'Skuntank', 'Bronzor', 'Bronzong', 'Bonsly', 'Mime Jr', 'Happiny', 'Chatot', 'Spiritomb', 'Gible', 'Gabite', 'Garchomp', 'Munchlax', 'Riolu', 'Lucario', 'Hippopotas', 'Hippowdon', 'Skorupi', 'Drapion', 'Croagunk', 'Toxicroak', 'Carnivine', 'Finneon', 'Lumineon', 'Mantyke', 'Snover', 'Abomasnow', 'Weavile', 'Magnezone', 'Lickilicky', 'Rhyperior', 'Tangrowth', 'Electivire', 'Magmortar', 'Togekiss', 'Yanmega', 'Leafeon', 'Glaceon', 'Gliscor', 'Mamoswine', 'PorygonZ', 'Gallade', 'Probopass', 'Dusknoir', 'Froslass', 'Rotom', 'Uxie', 'Mesprit', 'Azelf', 'Dialga', 'Palkia', 'Heatran', 'Regigigas', 'Giratina', 'Cresselia', 'Phione', 'Manaphy', 'Darkrai', 'Shaymin', 'Arceus', 'Victini', 'Snivy', 'Servine', 'Serperior', 'Tepig', 'Pignite', 'Emboar', 'Oshawott', 'Dewott', 'Samurott', 'Patrat', 'Watchog', 'Lillipup', 'Herdier', 'Stoutland', 'Purrloin', 'Liepard', 'Pansage', 'Simisage', 'Pansear', 'Simisear', 'Panpour', 'Simipour', 'Munna', 'Musharna', 'Pidove', 'Tranquill', 'Unfezant', 'Blitzle', 'Zebstrika', 'Roggenrola', 'Boldore', 'Gigalith', 'Woobat', 'Swoobat', 'Drilbur', 'Excadrill', 'Audino', 'Timburr', 'Gurdurr', 'Conkeldurr', 'Tympole', 'Palpitoad', 'Seismitoad', 'Throh', 'Sawk', 'Sewaddle', 'Swadloon', 'Leavanny', 'Venipede', 'Whirlipede', 'Scolipede', 'Cottonee', 'Whimsicott', 'Petilil', 'Lilligant', 'Basculin', 'Sandile', 'Krokorok', 'Krookodile', 'Darumaka', 'Darmanitan', 'Maractus', 'Dwebble', 'Crustle', 'Scraggy', 'Scrafty', 'Sigilyph', 'Yamask', 'Cofagrigus', 'Tirtouga', 'Carracosta', 'Archen', 'Archeops', 'Trubbish', 'Garbodor', 'Zorua', 'Zoroark', 'Minccino', 'Cinccino', 'Gothita', 'Gothorita', 'Gothitelle', 'Solosis', 'Duosion', 'Reuniclus', 'Ducklett', 'Swanna', 'Vanillite', 'Vanillish', 'Vanilluxe', 'Deerling', 'Sawsbuck', 'Emolga', 'Karrablast', 'Escavalier', 'Foongus', 'Amoonguss', 'Frillish', 'Jellicent', 'Alomomola', 'Joltik', 'Galvantula', 'Ferroseed', 'Ferrothorn', 'Klink', 'Klang', 'Klinklang', 'Tynamo', 'Eelektrik', 'Eelektross', 'Elgyem', 'Beheeyem', 'Litwick', 'Lampent', 'Chandelure', 'Axew', 'Fraxure', 'Haxorus', 'Cubchoo', 'Beartic', 'Cryogonal', 'Shelmet', 'Accelgor', 'Stunfisk', 'Mienfoo', 'Mienshao', 'Druddigon', 'Golett', 'Golurk', 'Pawniard', 'Bisharp', 'Bouffalant', 'Rufflet', 'Braviary', 'Vullaby', 'Mandibuzz', 'Heatmor', 'Durant', 'Deino', 'Zweilous', 'Hydreigon', 'Larvesta', 'Volcarona', 'Cobalion', 'Terrakion', 'Virizion', 'Tornadus', 'Thundurus', 'Reshiram', 'Zekrom', 'Landorus', 'Kyurem', 'Keldeo', 'Meloetta', 'Genesect', 'Chespin', 'Quilladin', 'Chesnaught', 'Fennekin', 'Braixen', 'Delphox', 'Froakie', 'Frogadier', 'Greninja', 'Bunnelby', 'Diggersby', 'Fletchling', 'Fletchinder', 'Talonflame', 'Scatterbug', 'Spewpa', 'Vivillon', 'Litleo', 'Pyroar', 'Flabebe', 'Floette', 'Florges', 'Skiddo', 'Gogoat', 'Pancham', 'Pangoro', 'Furfrou', 'Espurr', 'Meowstic', 'Honedge', 'Doublade', 'Aegislash', 'Spritzee', 'Aromatisse', 'Swirlix', 'Slurpuff', 'Inkay', 'Malamar', 'Binacle', 'Barbaracle', 'Skrelp', 'Dragalge', 'Clauncher', 'Clawitzer', 'Helioptile', 'Heliolisk', 'Tyrunt', 'Tyrantrum', 'Amaura', 'Aurorus', 'Sylveon', 'Hawlucha', 'Dedenne', 'Carbink', 'Goomy', 'Sliggoo', 'Goodra', 'Klefki', 'Phantump', 'Trevenant', 'Pumpkaboo', 'Gourgeist', 'Bergmite', 'Avalugg', 'Noibat', 'Noivern', 'Xerneas', 'Yveltal', 'Zygarde', 'Diancie', 'Hoopa', 'Volcanion', 'Rowlet', 'Dartrix', 'Decidueye', 'Litten', 'Torracat', 'Incineroar', 'Popplio', 'Brionne', 'Primarina', 'Pikipek', 'Trumbeak', 'Toucannon', 'Yungoos', 'Gumshoos', 'Grubbin', 'Charjabug', 'Vikavolt', 'Crabrawler', 'Crabominable', 'Oricorio', 'Cutiefly', 'Ribombee', 'Rockruff', 'Lycanroc', 'Wishiwashi', 'Mareanie', 'Toxapex', 'Mudbray', 'Mudsdale', 'Dewpider', 'Araquanid', 'Fomantis', 'Lurantis', 'Morelull', 'Shiinotic', 'Salandit', 'Salazzle', 'Stufful', 'Bewear', 'Bounsweet', 'Steenee', 'Tsareena', 'Comfey', 'Oranguru', 'Passimian', 'Wimpod', 'Golisopod', 'Sandygast', 'Palossand', 'Pyukumuku', 'Type Null', 'Silvally', 'Minior', 'Komala', 'Turtonator', 'Togedemaru', 'Mimikyu', 'Bruxish', 'Drampa', 'Dhelmise', 'Jangmo', 'Hakamo', 'Kommo', 'Tapu Koko', 'Tapu Lele', 'Tapu Bulu', 'Tapu Fini', 'Cosmog', 'Cosmoem', 'Solgaleo', 'Lunala', 'Nihilego', 'Buzzwole', 'Pheromosa', 'Xurkitree', 'Celesteela', 'Kartana', 'Guzzlord', 'Necrozma', 'Magearna', 'Marshadow', 'Poipole', 'Naganadel', 'Stakataka', 'Blacephalon', 'Zeraora', 'Meltan', 'Melmetal', 'Grookey', 'Thwackey', 'Rillaboom', 'Scorbunny', 'Raboot', 'Cinderace', 'Sobble', 'Drizzile', 'Inteleon', 'Skwovet', 'Greedent', 'Rookidee', 'Corvisquire', 'Corviknight', 'Blipbug', 'Dottler', 'Orbeetle', 'Nickit', 'Thievul', 'Gossifleur', 'Eldegoss', 'Wooloo', 'Dubwool', 'Chewtle', 'Drednaw', 'Yamper', 'Boltund', 'Rolycoly', 'Carkol', 'Coalossal', 'Applin', 'Flapple', 'Appletun', 'Silicobra', 'Sandaconda', 'Cramorant', 'Arrokuda', 'Barraskewda', 'Toxel', 'Toxtricity', 'Sizzlipede', 'Centiskorch', 'Clobbopus', 'Grapploct', 'Sinistea', 'Polteageist', 'Hatenna', 'Hattrem', 'Hatterene', 'Impidimp', 'Morgrem', 'Grimmsnarl', 'Obstagoon', 'Perrserker', 'Cursola', 'Sirfetched', 'Rime', 'Runerigus', 'Milcery','Alcremie', 'Falinks', 'Pincurchin', 'Snom', 'Frosmoth', 'Stonjourner', 'Eiscue', 'Indeedee', 'Morpeko', 'Cufant', 'Copperajah', 'Dracozolt', 'Arctozolt', 'Dracovish', 'Arctovish', 'Duraludon', 'Dreepy', 'Drakloak', 'Dragapult', 'Zacian', 'Zamazenta', 'Eternatus', 'Kubfu', 'Urshifu', 'Zarude', 'Regieleki', 'Regidrago', 'Glastrier', 'Spectrier', 'Calyrex', 'Hydra']
for i in range(len(allpkm)):
    var = 0
    for j in allpkm[i]:
        if j in ('a','e','i','o','u'):
            allpkm[i] = allpkm[i][:var+1] +','+ allpkm[i][var+1:]
            var+=1
        var+=1 
for i in range(len(allpkm)):
    allpkm[i] = allpkm[i].split(',')
sylables = [[],[],[],[],[],[]]
for i in range(len(allpkm)):
    for j in range(len(allpkm[i])):
        if allpkm[i][j] != '':
            sylables[j].append(allpkm[i][j])
    
def randName():
    global sylables
    rang = random.randint(len(sylables[0])+len(sylables[2])+10,len(sylables[0])+len(sylables[1])+len(sylables[2])+len(sylables[3])+len(sylables[4])+len(sylables[5]))
    while True:
        name = ''
        if rang < len(sylables[0])+len(sylables[1]):
            for i in range(2):
                name += sylables[i][random.randint(0,len(sylables[i])-1)]
        elif rang < len(sylables[0])+len(sylables[1])+len(sylables[2]):
            for i in range(3):
                name += sylables[i][random.randint(0,len(sylables[i])-1)]
        elif rang < len(sylables[0])+len(sylables[1])+len(sylables[2])+len(sylables[3]):
            for i in range(4):
                name += sylables[i][random.randint(0,len(sylables[i])-1)]
        elif rang < len(sylables[0])+len(sylables[1])+len(sylables[2])+len(sylables[3])+len(sylables[4]):
            for i in range(5):
                name += sylables[i][random.randint(0,len(sylables[i])-1)]
        else:
            for i in range(6):
                name += sylables[i][random.randint(0,len(sylables[i])-1)]
        var = 0
        var2 = 0
        for i in name:
            if i not in {'a','e','i','o','u'}:
                var += 1
            else: var2+=1
        if var >= 3 and (var2>=3 or random.randint(1,2) == 1) and len(name) < 10: break
    for i in range(len(name)): # double double letter checker
        if name[i] == name[i-1] and name[i-2] == name[i-3]:
            return randName()
    return name

def bitmonMaker():
    s1,s2,s3,s4,s5,s6,su1,su2,su3,su4,su5,su6 = 0,0,0,0,0,0,0,0,0,0,0,0
    stat, statup = [s1,s2,s3,s4,s5,s6], [su1,su2,su3,su4,su5,su6]
    for _ in range(105+random.randint(0,5)+random.randint(0,5)):
        stat[random.randint(0,5)] += 1
    for _ in range(152+random.randint(0,10)):
        statup[random.randint(0,5)] += 1
    numOfColour = 2
    for i in range(len(statup)):
        statup[i] = statup[i]/10
        if statup[i] > 3: numOfColour += 1
    colourList = [0,0,0]
    for _ in range(numOfColour):
        colourList[random.randint(0,2)] += 1
    if random.randint(1,10) <= 4: pkmtype = random.randint(0,5)
    elif random.randint(1,2) == 1: pkmtype = [0,2,1][colourList.index(max(colourList))]
    else: 
        if 0 == colourList.index(max(colourList)): pkmtype = random.randint(4,5)
        elif 1 == colourList.index(max(colourList)): pkmtype = random.randint(3,4)
        else: pkmtype = [3,5][random.randint(0,1)]
    movesPool = [['Rest',0,-10,6]]
    var1 = random.randint(0,6)
    movesPool.append(setupmoves()[0][var1][random.randint(0,len(setupmoves()[0][var1])-1)])
    for i in range(2): movesPool.append(setupmoves()[1][[pkmtype,random.randint(0,5)][i]][random.randint(0,len(setupmoves()[1][0])-1)])
    movesPool.append([setupmoves()[1][random.randint(0,5)][random.randint(0,len(setupmoves()[1][0])-1)],setupmoves()[2][pkmtype][random.randint(0,len(setupmoves()[2][0])-1)]][random.randint(0,1)])
    while movesPool[2] == movesPool[3] or movesPool[3] == movesPool[4]: movesPool[3] = setupmoves()[1][random.randint(0,5)][random.randint(0,len(setupmoves()[1][0])-1)]
    while movesPool[2] == movesPool[4]: movesPool[4] = setupmoves()[1][random.randint(0,5)][random.randint(0,len(setupmoves()[1][0])-1)]
    levelMovePool = [0,0]
    levelMovePool.append(random.randint(5,7))
    levelMovePool.append(random.randint(9,14))
    if movesPool[3] in setupmoves()[1][pkmtype]: levelMovePool.append(random.randint(16,20))
    else: levelMovePool.append(random.randint(19,24))
    if random.randint(1,3) == 1:
        if random.randint(1,4) == 1:
            if pkmtype == 2: movesPool.append(['Synthesis',10,-20,2])
            elif pkmtype == 3: movesPool.append(['Shadow Sleep',15,-16,5])
            else: movesPool.append(['Regenerate',4,35,6])
        else: movesPool.append([['Nap',2,-17,6],['Nap',2,-17,6],['Sleep',3,-23,6]][random.randint(0,2)])
        levelMovePool.append(random.randint(26,30))
    evoAt = random.randint(28,35)
    return BitmonClass(randName(),1,0,['Fire','Water','Plant','Air','Electric','Dark','Normal'][pkmtype],stat[0],stat[1],stat[2],stat[3],stat[4],stat[5]/2,statup[0],statup[1],statup[2],statup[3],statup[4],round(statup[5]/1.5,1),colourList,evoAt,movesPool,levelMovePool,['M','F'][random.randint(0,1)], drawNewBitmon())


def makeRandomRoom(size, start, end, maxLength = 0):
    directions = ((0,-1), (1,0), (0,1), (-1,0))
    for p in range(100):
        grid = [[random.randint(1,8) for _ in range(size[1])] for _ in range(size[0])]
        grid[end[0]][end[1]] = 0
        pos = [end]
        head = list(start[:])
        for _ in range(size[0]*size[1] if maxLength == 0 else maxLength):
            if head not in pos:
                pos.append(head[:])
            possibleMoves = []
            for i in directions:
                nextHead = head[:]
                nextHead[0] += i[0]
                nextHead[1] += i[1]
                try: 
                    if nextHead[0] < 0 or nextHead[1] < 0: raise 1
                    possibleMoves.append(grid[nextHead[0]][nextHead[1]])
                    grid[nextHead[0]][nextHead[1]] = 9
                except: possibleMoves.append(10)
            grid[head[0]][head[1]] = 9
            head[0] += directions[possibleMoves.index(min(possibleMoves))][0]
            head[1] += directions[possibleMoves.index(min(possibleMoves))][1]
            if head == list(end):
                grid = [[random.randint(0,2) for _ in range(size[1])] for _ in range(size[0])]
                for i in pos:
                    grid[i[0]][i[1]] = random.randint(0, 1)
                return grid 

    raise RuntimeError('Could not compute a reasonable path of length ' + str(maxLength if maxLength != 0 else size[0]*size[1]))

def createDungeon():
    global room, dungeonLayout, currentRoom
    dungeonLayout = [0, random.choice((0,1,3))]
    for i in range(random.randint(3, 6)):
        dungeonLayout.append((random.choice([0,1,3]) + dungeonLayout[i+1])%4)
    currentRoom = 0
    dungeonLayout.append(0)
    nextRoom()

def nextRoom():
    global room, dungeonLayout, currentRoom, portalPosition, currentFloor
    currentRoom += 1
    portalPosition = ((9+random.randint(-1, 1),0),(18,4+random.randint(-1, 1)),(9+random.randint(-1, 1),8),(0,4+random.randint(-1, 1)))[dungeonLayout[currentRoom]]
    character.x, character.y = ((9,8),(0,4),(9,0),(18,4))[dungeonLayout[currentRoom-1]]
    if len(dungeonLayout)-1 == currentRoom:
        room = [[0 for i in range(9)] for j in range(19)]
        portalPosition = (7, 4)
    else:
        room = makeRandomRoom((19,9), (character.x, character.y), portalPosition)

def loadHome():
    global character, room, world, portalPosition
    world = 'Home'
    character.x, character.y = 9,4
    room = [[0 for _ in range(20)] for _ in range(20)]
    portalPosition = 9, 0

def worldHandler():
    global world, character, portalPosition, currentFloor, gotoBitmonMenu
    if world == 'Home':
        if character.x == portalPosition[0] and character.y == portalPosition[1]:
            world = 'Dungeon'
            currentFloor = 1
            createDungeon()
            character.x, character.y = 9,8
        if gotoBitmonMenu:
            gotoBitmonMenu = False
            bitmonMenu(character.allBitmon)
    if world == 'Dungeon':
        if gotoBitmonMenu:
            gotoBitmonMenu = False
            bitmonMenu(character.bitmonTeam)
        if portalPosition == (7, 4):
            if (character.x, character.y) == (7, 4):
                createDungeon()
                currentFloor += 1
                character.x, character.y = 9,4
            elif (character.x, character.y) == (11, 4):
                loadHome()
        elif character.x == portalPosition[0] and character.y == portalPosition[1]:
            world = 'Dungeon'
            nextRoom()

def drawNewBitmon():
    global legsF, legsB, body, head
    colors = []
    for i in range(3):
        C = [0,0,0]
        while True:
            if sum(C) > (40,40,200)[i]: break
            for i in range(3): C[i] = random.randint(0,255) 
        for i in range(3):
            C[i] = C[i]/255
        colors.append(C)

    body = pygame.image.load(__file__[:-len(__file__.split('\\')[-1])] + 'Assets\\bitmon\\Body'+str(random.randint(1, 12))+'.png')
    head = pygame.image.load(__file__[:-len(__file__.split('\\')[-1])] + 'Assets\\bitmon\\Head'+str(random.randint(1, 15))+'.png')
    legVar = random.randint(1, 9)
    legsF = pygame.image.load(__file__[:-len(__file__.split('\\')[-1])] + 'Assets\\bitmon\\LegsF'+str(legVar)+'.png')
    legsB = pygame.image.load(__file__[:-len(__file__.split('\\')[-1])] + 'Assets\\bitmon\\LegsB'+str(legVar)+'.png')

    def invert(img):
        for i in range(32):
            for j in range(32):
                color = img.get_at((i,j))
                if sum(color) > 15 and color[3] > 255:
                    pygame.draw.rect(img, (color[2], color[1], color[0]), (i,j,1,1))
        return img

    if random.randint(0, 1) == 1:
        body = invert(body)
    if random.randint(0, 1) == 1:
        head = invert(head)
    wingList = (5,7)
    ifwings = random.randint(0, 50) == 1 and legVar not in wingList
    wings = random.choice(wingList)
    surface = pygame.image.load(__file__[:-len(__file__.split('\\')[-1])] + 'Assets\\bitmon\\template.png')
    animationTemp = (((0,0), (-1,0), (0,-1), (0,0)), ((0,0), (-1,0), (-1,-1), (0,-1)), ((0,0), (0,-1), (-1,0), (0,0)), ((0,0), (1,0), (1,1), (0,1)))
    for ir, i in enumerate(random.choice(animationTemp)):
        surface.blit(legsB, (32*ir,0))
        if ifwings:
            surface.blit(pygame.image.load(__file__[:-len(__file__.split('\\')[-1])] + 'Assets\\bitmon\\LegsB'+str(wings)+'.png'), (32*ir+i[0],i[1]))
            surface.blit(body, (32*ir+i[0],i[1]))
            surface.blit(pygame.image.load(__file__[:-len(__file__.split('\\')[-1])] + 'Assets\\bitmon\\LegsF'+str(wings)+'.png'), (32*ir+i[0],i[1]))
        else: surface.blit(body, (32*ir+i[0],i[1]))
        surface.blit(head, (32*ir+i[0],i[1]))
        surface.blit(legsF, (32*ir,0))

    for i in range(128):
        for j in range(32):
            color = surface.get_at((i,j))
            if color[3] != 255: continue
            if color[0] >= 10 and color[1] <= 55 and color[2] <= 55:
                pygame.draw.rect(surface, (color[0]*colors[0][0], color[0]*colors[0][1], color[0]*colors[0][2]), (i,j,1,1))
            elif color[0] <= 55 and color[1] >= 10 and color[2] <= 55:
                pygame.draw.rect(surface, (color[1]*colors[1][0], color[1]*colors[1][1], color[1]*colors[1][2]), (i,j,1,1))
            elif color[0] <= 55 and color[1] <= 55 and color[2] >= 10:
                pygame.draw.rect(surface, (color[2]*colors[2][0], color[2]*colors[2][1], color[2]*colors[2][2]), (i,j,1,1))
    return surface

def escMenu():
    global running, gotoBitmonMenu
    w,s,e = False,False,False
    selection = 0
    text = ['Bitmon', 'Inventory', 'Hatchery', 'Mixing', 'Exit']
    for i in range(5): text[i] = pygame.font.SysFont('powerclear', 90).render(text[i], True, [(125,205,255), (255,255,255),(255,205,100),(150,255,150),(255,100,100)][i])
    textInv = ['Gold : {}'.format(gameSave['gold']), 'Eggs : {}'.format(gameSave['eggs']), 'R : {}'.format(gameSave['color'][0]), 'G : {}'.format(gameSave['color'][1]), 'B : {}'.format(gameSave['color'][2])]
    for i in range(5): textInv[i] = pygame.font.SysFont('powerclear', 90).render(textInv[i], True, (255,255,255))
    textHat = ['Hatchery', 'Eggs : {}'.format(gameSave['eggs']), 'Gold : {}'.format(gameSave['gold']), 'Hatch', 'Exit']
    for i in range(5): 
        textHat[i] = pygame.font.SysFont('powerclear', 90).render(textHat[i], True, [(255,235,150), (255,255,255),(255,255,255),(255,255,255),(255,150,150)][i])
    inInventory = False
    inHatchery = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q: return
                if event.key == pygame.K_w or event.key == pygame.K_UP: w = True
                if event.key == pygame.K_s or event.key == pygame.K_DOWN: s = True
                if event.key == pygame.K_e or event.key == pygame.K_SPACE: e = True

        if s:
            s = False
            selection += 1
            if selection >= 5: selection = 0
        if w:
            w = False
            selection -=1
            if selection < 0: selection = 4
        if e:
            e = False
            if inInventory: 
                inInventory = False
                continue
            elif inHatchery:
                if selection == 4:
                    inHatchery = False
                    continue
            else:
                if selection == 0:
                    gotoBitmonMenu = True
                    return
                if selection == 1:
                    inInventory = True
                if selection == 2:
                    inHatchery = True
                if selection == 4:
                    running = False
                    return
        # draw
        pygame.draw.rect(SCREEN, (20,20,30), (1345, 45, 410, 600))
        pygame.draw.rect(SCREEN, (50,50,55), (1350, 50, 400, 590))
        pygame.draw.rect(SCREEN, (75,75,80), (1355, 55+120*selection, 390, 100))
        for i in range(5):
            if inInventory: SCREEN.blit(textInv[i], (1360, 75+120*i))
            elif inHatchery: SCREEN.blit(textHat[i], (1360, 75+120*i))
            else: SCREEN.blit(text[i], (1360, 75+120*i))
        pygame.display.update()

def bitmonMenu(bitmonList):
    global running, SCREEN
    pageNum = 0
    selection = 0
    selectedBitmon = None
    monPerPage = 10
    typeColors = {'Fire':(255,150,80), 'Water':(80,150,232),'Plant':(160,255,140),'Air':(190,220,255),'Electric':(240,240,100),'Dark':(120,120,150),'Normal':(255,255,255)}
    animationFrame = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    return
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    selection -= 1
                    if selection < 0: selection = len(bitmonList)%monPerPage-1 if (pageNum+1)*monPerPage > len(bitmonList) else monPerPage-1
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    selection += 1
                    if selection == monPerPage or selection+pageNum*monPerPage >= len(bitmonList): selection = 0
                if event.key == pygame.K_SPACE:
                    selectedBitmon = bitmonList[selection+monPerPage*pageNum]
                if event.key == pygame.K_a:
                    pageNum = max(pageNum-1, 0)
                if event.key == pygame.K_d:
                    pageNum = min(pageNum+1, len(bitmonList)//monPerPage)
                    try: bitmonList[selection+monPerPage*pageNum]
                    except: selection = len(bitmonList)%monPerPage-1
        SCREEN.fill((10,15,25))
        pygame.draw.rect(SCREEN, (50,65,75), (5, 15+90*selection, 500, 80))
        if selectedBitmon:
            animationFrame = (animationFrame+1)%60
            SCREEN.blit(pygame.transform.scale(selectedBitmon.animation.subsurface(((animationFrame//15)*32, 0, 32, 32)),(640,640)),(600,30))
            SCREEN.blit(pygame.font.SysFont('powerclear', 100).render(selectedBitmon.name, True, (255,255,255)), (1260, 20))
            SCREEN.blit(pygame.font.SysFont('powerclear', 80).render(selectedBitmon.type, True, typeColors[selectedBitmon.type]), (1500, 105))
            SCREEN.blit(pygame.font.SysFont('powerclear', 70).render('lvl: ' + str(selectedBitmon.level), True, (255,255,255)), (1280, 108))
            SCREEN.blit(pygame.font.SysFont('powerclear', 80).render('Stats  |    per lvl', True, (255,255,255)), (1250, 230))
            SCREEN.blit(pygame.font.SysFont('powerclear', 70).render('Health      ' + str(round(selectedBitmon.health,1)) + ' | ' + str(round(selectedBitmon.Hup,1)), True, (205,255,205)), (1250, 330))
            SCREEN.blit(pygame.font.SysFont('powerclear', 70).render('Attack      ' + str(round(selectedBitmon.attack,1)) + ' | ' + str(round(selectedBitmon.Aup,1)), True, (255,200,200)), (1250, 410))
            SCREEN.blit(pygame.font.SysFont('powerclear', 70).render('Defence   ' + str(round(selectedBitmon.defence,1)) + ' | ' + str(round(selectedBitmon.Dup,1)), True, (205,200,255)), (1250, 490))
            SCREEN.blit(pygame.font.SysFont('powerclear', 70).render('Speed       ' + str(round(selectedBitmon.speed,1)) + ' | ' + str(round(selectedBitmon.Sup,1)), True, (255,255,200)), (1250, 570))
            SCREEN.blit(pygame.font.SysFont('powerclear', 70).render('Mana        ' + str(round(selectedBitmon.manaMax,1)) + ' | ' + str(round(selectedBitmon.MMup,1)), True, (200,255,255)), (1250, 650))
            SCREEN.blit(pygame.font.SysFont('powerclear', 70).render('Mana Fill  '+ str(round(selectedBitmon.manaFill,1)) + ' | ' + str(round(selectedBitmon.MFup,1)), True, (200,255,255)), (1250, 730))
            SCREEN.blit(pygame.font.SysFont('powerclear', 55).render('Exp', True, (255,255,255)), (1230, 170))
            pygame.draw.rect(SCREEN, (0,200,255), (1320, 180, 400*(selectedBitmon.exp/selectedBitmon.expToLevel()), 20), 10, 5)
            pygame.draw.rect(SCREEN, (0,60,65), (1320, 180, 400, 20), 2, 5)
            SCREEN.blit(textures.arrow, (1487,248))
            SCREEN.blit(pygame.transform.scale({'M':textures.male, 'F':textures.female}[selectedBitmon.gender], (56,74)), (1700,30))

        for i in range(monPerPage):
            try:
                bitmon = bitmonList[i+monPerPage*pageNum]
                text = pygame.font.SysFont('powerclear', 80).render(str(bitmon.level) + ' - ' + bitmon.name, True, typeColors[bitmon.type])
                SCREEN.blit(text, (20,20+90*i))
            except: pass
        clock.tick(60)
        pygame.display.update()

def draw():
    SCREEN.fill((10,13,18))
    if world == 'Home': 
        SCREEN.blit(textures.homebg, (0,0))
        SCREEN.blit(textures.resize(textures.portal, (150,150)), (800, 30))
    if world == 'Dungeon': 
        SCREEN.blit(textures.dungeonbg, (0,0))
        for ir, i in enumerate(room):
            for jr, j in enumerate(i):
                if j == 2: SCREEN.blit(textures.resize(textures.rock, (90,90)), (90*(ir+0.3),90*(jr+0.9)))
                elif j == 1: SCREEN.blit(textures.resize(textures.grass, (90,90)), (90*(ir+0.3),90*(jr+0.9)))
        if portalPosition == (7, 4): SCREEN.blit(textures.resize(textures.regularDoor, (150, 150)), (990, 360))
        SCREEN.blit(textures.resize(textures.portal, (150,150)), (portalPosition[0]*90, portalPosition[1]*90))

    SCREEN.blit(pygame.transform.scale(character.frame, (150, 150)), (character.x*90, character.y*90))
    pygame.display.update()

a,d,w,s = False,False,False,False
character = player(textures.playerWalk, 9, 4)
clock = pygame.time.Clock()
world = 'Home'
portalPosition = 9, 0
running = True
room = [[0 for _ in range(20)] for _ in range(20)]
currentFloor = 0
gotoBitmonMenu = False

if character.allBitmon == []:
    for i in range(4):
        character.addBitmon(bitmonMaker().levelUp(random.choice((0,0,1,1,1,1,2))))


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: character.x, character.y = portalPosition
            if event.key == pygame.K_a: a = True
            if event.key == pygame.K_d: d = True
            if event.key == pygame.K_w: w = True
            if event.key == pygame.K_s: s = True
            if event.key == pygame.K_LSHIFT: character.sprinting = True
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_e: 
                var = escMenu()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a: a = False
            if event.key == pygame.K_d: d = False
            if event.key == pygame.K_w: w = False
            if event.key == pygame.K_s: s = False
            if event.key == pygame.K_LSHIFT: character.sprinting = False
    
    if w: character.move(0)
    elif d: character.move(1)
    elif s: character.move(2)
    elif a: character.move(3)

    worldHandler()
    textures.frameUpdate()
    draw()
    clock.tick(60)
