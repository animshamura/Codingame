import sys
import math

# Survive the attack waves

# map parser, not needed to change at all
player_id = int(input())
width, height = [int(i) for i in input().split()]
game_map = []
for i in range(height):
    line = input()
    game_map.append(line)

# do not change if beginner, this takes all the game inputs and parses them for ease of use
def process_input():
    my_money, my_lives = [int(i) for i in input().split()]
    opponent_money, opponent_lives = [int(i) for i in input().split()]
    
    towers = []
    attackers = []

    tower_count = int(input())
    for i in range(tower_count):
        inputs = input().split()
        tower_type = inputs[0]
        tower_id = int(inputs[1])
        owner = int(inputs[2])
        x = int(inputs[3])
        y = int(inputs[4])
        damage = int(inputs[5])
        attack_range = float(inputs[6])
        reload = int(inputs[7])
        cool_down = int(inputs[8])
        tower = {
            "towerType": tower_type,
            "towerId": tower_id,
            "owner": owner,
            "x": x,
            "y": y,
            "damage": damage,
            "range": attack_range,
            "reload": reload,
            "coolDown": cool_down
        }
        towers.append(tower)


    attacker_count = int(input())
    for i in range(attacker_count):
        inputs = input().split()
        attacker_id = int(inputs[0])
        owner = int(inputs[1])
        x = float(inputs[2])
        y = float(inputs[3])
        hit_points = int(inputs[4])
        max_hit_points = int(inputs[5])
        current_speed = float(inputs[6])
        max_speed = float(inputs[7])
        slow_time = int(inputs[8])
        bounty = int(inputs[9])
        attacker = {
            "attackerId": attacker_id,
            "owner": owner,
            "x": x,
            "y": y,
            "hitPoints": hit_points,
            "maxHitPoints": max_hit_points,
            "currentSpeed": current_speed,
            "maxSpeed": max_speed,
            "slowTime": slow_time,
            "bounty": bounty
        }
        attackers.append(attacker)

    return [ my_money, my_lives, opponent_money, opponent_lives, tower_count, towers, attackers ]


# prints some message in the console for debugging
def print_debug(message):
    print(f"{message}", file=sys.stderr, flush=True)


# checks if the block at (x,y) coordinate is a canyon or plateu
# return '#' for plateu and '.' for canyon
# Note that you can only build towers if a block is a canyon
def get_coordinate(x, y):

    if( width <= x ):
        print_debug(f"{x} is invalid because its greater than width={width}")
        raise Exception(f"{x} is invalid because its greater than width={width}")
    if( x < 0 ):
        print_debug(f"{x} is invalid because its negative")
        raise Exception(f"{x} is invalid because its negative")
    
    if( height <= y ):
        print_debug(f"{y} is invalid because its greater than height={height}")
        raise Exception(f"{y} is invalid because its greater than height={height}")
    if( y < 0 ):
        print_debug(f"{y} is invalid because its negative")
        raise Exception(f"{y} is invalid because its negative")
    
    return game_map[y][x]



# returns if the block at (x,y) coordinate already has a tower built at this location
# you can't build a tower on a block that already contains another tower
# Note that, you also have to pass the towers array into this function
def check_if_block_is_occupied(x, y, towers):
    for tower in towers:
        if tower["x"] == x and tower["y"] == y:
            return True
    return False


# This function prints all information about towers currently active in the map
def print_towers(towers):
    for tower in towers:
        print("Tower {index}:", file=sys.stderr, flush=True)
        print(tower, file=sys.stderr, flush=True)

        
# This function prints all information about attackers currently active in the map
def print_attackers(attackers):
    for attacker in attackers:
        print("Attacker {index}:", file=sys.stderr, flush=True)
        print(attacker, file=sys.stderr, flush=True)


# print gamee map
def print_game_map(game_map):
    for i in game_map:
        print(i, file=sys.stderr, flush=True)



turn = 0


# tower_states contains information about which upgrade stage a tower is at
# tower_states = {
#     "{id}": {upgrade_stage (1/2/3) },
# }
tower_states = {}

# my_money, my_lives, opponent_money, opponent_lives, tower_count, towers, attackers = (0,0,0,0,0,[],[])

# game loop
while True:
    commands = []
    inputs = process_input()

    my_money, my_lives, opponent_money, opponent_lives, tower_count, towers, attackers = inputs

    def execute_commands():
        if len(commands) == 0:
            print("PASS")
        else:
            for i in range(len(commands)):
                if i == len(commands) - 1:
                    print(commands[i])
                else:
                    print(commands[i], end=";")
                
                
    # builds the desired tower at (x,y)
    def build_tower(x, y, tower_type):
        # print_debug(my_money)
        commands.append("BUILD " + str(x) + " " + str(y) + " " + tower_type)
        global my_money
        my_money -= 100 - ( 30 if tower_type == "GLUETOWER" else 0 )


    # upgrades the desired tower at (x,y)
    # upgrade_type can be DAMAGE / RELOAD / RANGE
    def upgrade_tower(x, y, upgrade_type):
        built = False
        for tower in towers:
            if tower["x"] == x and tower["y"] == y:
                if tower["owner"] != player_id:
                    print_debug(f"The tower at ({x},{y}) is not yours")
                    raise Exception(f"The tower at ({x},{y}) is not yours")
                    
                built = True
                if tower["towerId"] in tower_states:
                    tower_states[tower["towerId"]] = tower_states[tower["towerId"]] + 1
                else:
                    tower_states[tower["towerId"]] = 1
                
                global my_money
                my_money -= tower_states[tower["towerId"]] * 50
                
                commands.append("UPGRADE " + str(tower["towerId"]) + " " + upgrade_type) # upgrade_type can be DAMAGE, RANGE or RELOAD
        
        
        if built == False:
            print_debug(f"There is no tower at ({x},{y})")
            raise Exception(f"There is no tower at ({x},{y})")


    # When towercount > 5
    # Attempt block change



    # DEMO STRATEGY <You can remove this!>
    strategy = 1
    # this block of code finds 'empty' plateau at the immediate left side of a canyon and places a tower there
    if strategy == 1:
        for y in range(height):
            for x in range(width):
                if x+1 < width and get_coordinate(x, y) == '#' and get_coordinate(x+1, y) == '.' and not check_if_block_is_occupied(x,y,towers):
                    if my_money > 100:
                        build_tower(x, y, "GUNTOWER") # you can change this to GUNTOWER, FIRETOWER, GLUETOWER or HEALTOWER as necessary
                
        if my_money >= 50 and turn >= 2:
            for tower in towers:   
                if tower["owner"] == player_id:
                    upgrade_tower(tower["x"], tower["y"], "DAMAGE")

    # in this elif statement you can check if tower_count > 5 and only activate your 2nd strategy
    # if tower_count is greater than 5
    elif strategy == 2:
        pass
        # You could make your own code strategy here!
        # remove the "pass" statement when writing your own strategy
    
    execute_commands()
    turn = turn + 1
    

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    # BUILD x y TOWER | UPGRADE id PROPERTY
    # print("BUILD 5 5 GUNTOWER")
