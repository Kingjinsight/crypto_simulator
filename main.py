from board import *
from events import *
from player import *

print("You are a new student at the University of Edinburgh. Have fun at the best university in Scotland!")
print("However you need to ensure you don't run out of money while living here.\nYou will get £210 every week from Student Finance. Your rent is £150 a week, paid monthly.")
print("While you should save, you are here to have fun too, so make sure you don't penny pinch too hard.\n")

board = Board()
player = Player()

while True:
    if board.spaces[player.space].type == SpaceType.SALARY:
        player.balance += 210

    if board.spaces[player.space].type == SpaceType.RAND_EVENT:
        event(player, random.randint(1,22))
 
    player.status()
    next = input()

    player.next_day()