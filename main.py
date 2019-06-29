from colorama import Fore, Style
import pygame
import random


class Cell:
    def __init__(self, location=[0, 0]):
        self.location = location
        self.win = pygame.display.set_mode((1250, 625))
        self.win.fill((235, 235, 235))
        pygame.display.flip()
        pygame.draw.rect(self.win, (0, 0, 0), (12.5, 12.5, 600, 600)) # black border on the left side
        pygame.draw.rect(self.win, (255, 255, 255), (19.5, 19.5, 587, 587)) # white box on the left side
        pygame.draw.rect(self.win, (0, 0, 0), (630, 12.5, 600, 600)) # black box on the right side
        pygame.draw.rect(self.win, (255, 255, 255), (637, 19.5, 587, 587))# white box on the right side

    offset = 117.4
    start_x = 0
    start_y = 0
    center_x = 0
    center_y = 0
    third_x = 0
    third_y = 0
    north = 0
    south = 0
    east = 0
    west = 0
    here = False
    q_value = 1

    def set_north(self, value):
        self.north = value

    def set_south(self, value):
        self.south = value

    def set_east(self, value):
        self.east = value

    def set_west(self, value):
        self.west = value

    def here_now(self, op):
        self.here = op

    def output(self):
        print(self.location, end=" ")
        print(Style.RESET_ALL, end="")

    def fredOutput(self):
        print(Fore.YELLOW, end="")
        print(self.location, end=" ")
        print(Style.RESET_ALL, end="")

    def set_rectangle(self, v1, v2, v3, v4, v5, v6):
        self.start_x = v1
        self.start_y = v2
        self.center_x = v3
        self.center_y = v4
        self.third_x = v5
        self.third_y = v6

    def set_win(self, win):
        self.win = win

    def make_rectangle(self): # makes the green triangles on the board anf we can later change the colors by multiplying green by a scaler
        for i in range(0, 5):
            for j in range(0, 5):
                self.q_value = random.uniform(0, 1) # random int between 0 and 1 to just show changing colors; used for testing
                pygame.draw.polygon(self.win, (0, 255*self.q_value, 0),
                                    [[637 + i * offset, 19.5 + j * offset], [695.7 + i * offset, 78.2 + j * offset],
                                    [637 + i * offset, 136.9 + j * offset]])# draws a triangle on a quadrant of the square
                pygame.display.update()
                self.q_value = random.uniform(0, 1)
                pygame.draw.polygon(self.win, (0, 255*self.q_value, 0),
                                    [[754.4 + i * offset, 19.5 + j * offset], [695.7 + i * offset, 78.2 + j * offset],
                                    [754.4 + i * offset, 136.9 + j * offset]])
                pygame.display.update()
                self.q_value = random.uniform(0, 1)
                pygame.draw.polygon(self.win, (0, 255*self.q_value, 0),
                                    [[637 + i * offset, 19.5 + j * offset], [695.7 + i * offset, 78.2 + j * offset],
                                    [754.4 + i * offset, 19.5 + j * offset]])
                pygame.display.update()
                self.q_value = random.uniform(0, 1)
                pygame.draw.polygon(self.win, (0, 255*self.q_value, 0),
                                    [[754.4 + i * offset, 136.9 + j * offset], [695.7 + i * offset, 78.2 + j * offset],
                                    [637 + i * offset, 136.9 + j * offset]])
                pygame.display.update()


class Pickup(Cell): # a pickup cell is just a location on the board we can pickup blocks from
    def __init__(self, location=[0, 0], num_of_pack=0):
        Cell.__init__(self, location)
        super(Pickup, self).__init__()
        self.num_of_pack = num_of_pack

    def give(self, agent):# not really using this right now but does a check for if it can give one and gives a pack all in one
        if self.num_of_pack > 0 and agent.has_pack is False:
            agent.has_pack = True
            self.num_of_pack -= 1

    def output(self):
        print(Fore.GREEN, end="")
        print(self.location, end=" ")
        print(Style.RESET_ALL, end="")

    def take_pack(self):
        self.num_of_pack -= 1

    def can_take_pack(self):
        if self.num_of_pack > 0:
            return True
        return False



class DropOff(Cell):# used for dropping off blocks from the agent
    def __init__(self, location=[0, 0], num_of_pack=0):
        Cell.__init__(self, location)
        super(DropOff, self).__init__()
        self.num_of_pack = num_of_pack

    def drop(self, agent): # not really using this right now like in pickup with give
        if agent.has_pack is True:
            agent.has_pack = False
            self.num_of_pack += 1

    def output(self):
        print(Fore.RED, end="")
        print(self.location, end=" ")
        print(Style.RESET_ALL, end="")

    def give_pack(self):
        self.num_of_pack += 1

    def can_give_pack(self):
        if self.num_of_pack < 5:
            return True
        return False

class Agent: # agent used for traversing the board
    def __init__(self, location=[0, 0], has_pack=False, reward=0):
        self.location = location
        self.has_pack = has_pack
        self.reward = reward

    def output(self):# used for testing i think
        print(Fore.YELLOW, end="")
        print(self.location, end="")
        print(Style.RESET_ALL, end="")

    def give_pack(self):# can only hold 1 pack at a time so pack is a bool
        self.has_pack = True

    def take_pack(self):
        self.has_pack = False

    def same_location(self, a):# used to compare locations
        if self.location == a:
            return True
        else:
            return False

    def can_pickup(self): #checks if it can pickup at this location
        if not self.has_pack:
            if isinstance(pd_world[self.location[0]][self.location[1]], Pickup):
                return True
            else:
                return False
        else:
            return False

    def can_dropoff(self):# checks if it can dropoff at this location based on type to prevent breaking
        if self.has_pack:
            if isinstance(pd_world[self.location[0]][self.location[1]], DropOff):
                return True
            else:
                return False
        else:
            return False

    def move_north(self):# moves north
        if self.location[0] > 0:
            self.location[0] -= 1

    def move_east(self):# moves east
        if self.location[1] < 4:
            self.location[1] += 1

    def move_south(self):# moves south
        if self.location[0] < 4:
            self.location[0] += 1

    def move_west(self):#moves west
        if self.location[1] > 0:
            self.location[1] -= 1

    def can_move_north(self):#checks to see if it can move north i.e. not in the first row
        if self.location[0] > 0:
            return True
        else:
            return False

    def can_move_east(self):
        if self.location[1] < 4:
            return True
        else:
            return False

    def can_move_south(self):
        if self.location[0] < 4:
            return True
        else:
            return False

    def can_move_west(self):
        if self.location[1] > 0:
            return True
        else:
            return False

    def move_random(self):# PRandom
        print(self.location)
        done = False
        while not done:
            spot = -1
            a = random.randint(0, 3)
            if self.check_for_operator(spot):
                break
            if spot == a:
                while spot == a:
                    a = random.randint(0, 3)
            elif a == 0 and self.can_move_north():
                self.move_north()
                done = True
            elif a == 1 and self.can_move_east():
                self.move_east()
                done = True
            elif a == 2 and self.can_move_south():
                self.move_south()
                done = True
            elif a == 3 and self.can_move_west():
                self.move_west()
                done = True

    def check_for_operator(self, way):  # checks if there's an applicable operator
        if self.can_move_north() and isinstance(pd_world[self.location[0]-1][self.location[1]], Pickup) and not self.has_pack:
            if pd_world[self.location[0]-1][self.location[1]].can_take_pack():
                self.move_north()
            # if we can take one then, take one
                pd_world[self.location[0]][self.location[1]].take_pack()
                self.give_pack()
                print('wooooooo')
                return True
            elif not pd_world[self.location[0]-1][self.location[1]].can_take_pack():
                way = 0
                return False
        if self.can_move_east() and isinstance(pd_world[self.location[0]][self.location[1]+1], Pickup) and not self.has_pack:
            if pd_world[self.location[0]][self.location[1]+1].can_take_pack():
                self.move_east()
                pd_world[self.location[0]][self.location[1]].take_pack()
                self.give_pack()
                print('whaaa')
                return True
            elif not pd_world[self.location[0]][self.location[1]+1].can_take_pack():
                way = 1
                return False
        if self.can_move_south() and isinstance(pd_world[self.location[0]+1][self.location[1]], Pickup) and not self.has_pack:
            if pd_world[self.location[0]+1][self.location[1]].can_take_pack():
                self.move_south()
                pd_world[self.location[0]][self.location[1]].take_pack()
                self.give_pack()
                print('osngl')
                return True
            elif not pd_world[self.location[0]+1][self.location[1]].can_take_pack():
                way = 2
                return False
        if self.can_move_west() and isinstance(pd_world[self.location[0]][self.location[1]-1], Pickup) and not self.has_pack:
            if pd_world[self.location[0]][self.location[1]-1].can_take_pack():
                self.move_west()
                pd_world[self.location[0]][self.location[1]].take_pack()
                self.give_pack()
                print('fjk')
                return True
            elif not pd_world[self.location[0]][self.location[1]-1].can_take_pack():
                way = 3
                return False
        if self.can_move_north() and isinstance(pd_world[self.location[0]-1][self.location[1]], DropOff) and self.has_pack:
            if pd_world[self.location[0]-1][self.location[1]].can_give_pack():
                self.move_north()
                pd_world[self.location[0]][self.location[1]].give_pack()
                self.take_pack()
                print('gkslagnjs')
                return True
            elif not pd_world[self.location[0]-1][self.location[1]].can_give_pack():
                way = 0
                return False
        if self.can_move_east() and isinstance(pd_world[self.location[0]][self.location[1]+1], DropOff) and self.has_pack:
            if pd_world[self.location[0]][self.location[1]+1].can_give_pack():
                self.move_east()
                pd_world[self.location[0]][self.location[1]].give_pack()
                self.take_pack()
                print('gnlksn')
                return True
            elif not pd_world[self.location[0]][self.location[1]+1].can_give_pack():
                way = 1
                return False
        if self.can_move_south() and isinstance(pd_world[self.location[0]+1][self.location[1]], DropOff) and self.has_pack:
            if pd_world[self.location[0]+1][self.location[1]].can_give_pack():
                self.move_south()
                pd_world[self.location[0]][self.location[1]].give_pack()
                self.take_pack()
                print('gnlsgnksa')
                return True
            elif not pd_world[self.location[0]+1][self.location[1]].can_give_pack():
                way = 2
                return False
        if self.can_move_west() and isinstance(pd_world[self.location[0]][self.location[1]-1], DropOff) and self.has_pack:
            if pd_world[self.location[0]][self.location[1]-1].can_give_pack():
                self.move_west()
                pd_world[self.location[0]][self.location[1]].give_pack()
                self.take_pack()
                print('alkgjkn')
                return True
            elif not pd_world[self.location[0]][self.location[1]-1].can_give_pack():
                way = 3
                return False


def outtie(world):#outputs current holding of pickup and dropoff locations
    print(world[0][0].num_of_pack)
    print(world[2][2].num_of_pack)
    print(world[4][4].num_of_pack)
    print(world[1][4].num_of_pack)
    print(world[4][0].num_of_pack)
    print(world[4][2].num_of_pack)


def done(world):# checks if the game is complete, will later add that if the agent has hit a score of 0 then the game is over
    counts = 0
    for i in range(0, 5):
        for j in range(0, 5):
            if isinstance(world[i][j], DropOff) and world[i][j].num_of_pack == 5 or isinstance(world[i][j], Pickup) and world[i][j].num_of_pack == 0:
                counts += 1
    if counts == 6:
        return True
    else:
        return False


def get_q_table():# still have to make this but will put the textfile q table into an array
    file = open("testfile.txt", "r")
    p = file.read()
    print(p)
    return p


# ----------------------------------------------------------------------------------------
# beginning of the main program
pd_world = [[Cell() for j in range(0, 5)] for i in range(0, 5)]


pd_world[0][0] = Pickup([0, 0], 5)
pd_world[2][2] = Pickup([2, 2], 5)
pd_world[4][4] = Pickup([4, 4], 5)

# creates the pickup cells

pd_world[1][4] = DropOff()
pd_world[4][0] = DropOff()
pd_world[4][2] = DropOff()
# creates the dropoff cells

fred = Agent([0, 4], False, 0)
# initialize the agent

for i in range(0, 5):
    for j in range(0, 5):
        pd_world[i][j].location = list((i, j))
        # assigns the correct location for each cell

# values \('.')/
start_x = 637
start_y = 19.5
center_x = 695.7
center_y = 78.2
third_x = 754.4
third_y = 136.9

# outputs the game board initially
for i in range(0, 5):
    for j in range(0, 5):
        if fred.same_location(pd_world[i][j].location):
            pd_world[i][j].fredOutput()
        elif isinstance(pd_world[i][j], Pickup):
            pd_world[i][j].output()
        elif isinstance(pd_world[i][j], DropOff):
            pd_world[i][j].output()
        else:
            pd_world[i][j].output()
    print('\n')

# -----------------------------------------------------------------------------

# win = pygame.display.set_mode((1250, 625))
running = True  # used for the game board gui

# this stuff below was just for testing

# width = 50
# height = 50
# x = 100
# y = 100
# while running:
#    for event in pygame.event.get():
#        if event.type == pygame.QUIT:
#            running = False
# each edge of teh triangle should be 130.1076 long


'''win.fill((235, 235, 235))
pygame.display.flip()
kid = pygame.draw.rect(win, (0, 0, 0), (12.5, 12.5, 600, 600))
pygame.draw.rect(win, (255, 255, 255), (19.5, 19.5, 587, 587))


pygame.draw.rect(win, (0, 0, 0), (630, 12.5, 600, 600))
pygame.draw.rect(win, (255, 255, 255), (637, 19.5, 587, 587))
'''

offset = 117.4
center_x = 766.72


arr = [(25, 55, 255), (255, 0, 255), (0, 255, 0), (0, 0, 255), (255, 0, 0), (50, 125, 125), (50, 125, 0), (125, 255, 50), (0, 125, 125), (50, 255, 50), (50, 50, 255), (255, 50, 50), (12, 55, 125), (125, 170, 79), (75, 75, 75), (55, 10, 200), (90, 255, 90), (120, 150, 20), (25, 0, 0), (125, 125, 125), (125, 125, 0), (255, 255, 255), (255, 0, 255), (0, 255, 0), (0, 0, 255), (255, 0, 0), (125, 125, 125), (125, 125, 0),]

count = 0
for i in range(0, 5):
    for j in range(0, 5):
        #pygame.draw.rect(win, arr[count], (637 + i*offset, 19.5 + j*offset, 117.4, 117.4), 5)
        count += 1
    pygame.display.flip()


colors = [[]]


'''
for i in range(0, 5):
    for j in range(0, 5):
        pd_world[i][j].make_rectangle()
        #pygame.draw.polygon(win, (255, 0, 0), [[637 + i*offset, 19.5 + j*offset], [695.7 + i*offset, 78.2 + j*offset], [637 + i*offset, 136.9 + j*offset]])
        #pygame.draw.polygon(win, (0, 255, 0), [[754.4 + i*offset, 19.5 + j*offset], [695.7 + i*offset, 78.2 + j*offset], [754.4 + i*offset, 136.9 + j*offset]])
        #pygame.draw.polygon(win, (0, 0, 255), [[637 + i*offset, 19.5 + j*offset], [695.7 + i*offset, 78.2 + j*offset], [754.4 + i*offset, 19.5 + j*offset]])
        #pygame.draw.polygon(win, (0, 0, 0), [[754.4 + i*offset, 136.9 + j*offset], [695.7 + i*offset, 78.2 + j*offset], [637 + i*offset, 136.9 + j*offset]])

# (left, right, up down)
'''

# this is the code for the green triangles if you un comment it you'll see the stuff above was just for testing
'''
while running:
    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    for i in range(0, 5):
        for j in range(0, 5):
            pd_world[i][j].make_rectangle()
    pygame.display.update()

get_q_table()  # just prints out the q table file
'''

print(done(pd_world))
outtie(pd_world)

cnt = 0

while not done(pd_world):
    fred.move_random()
    outtie(pd_world)
#    cnt += 1
#    if cnt == 150:  # used to cut the program early for testing
#        break

outtie(pd_world)


# find a way to store the q values after each run so that you can use them again the next run

# store current locations
# look at neighboring cells and depending on that

# create two different q tables
# one for when them carrying a block is true and one for when that is false



