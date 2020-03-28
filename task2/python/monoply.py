import random

random.seed(0) # don't touch!

# you are not allowed to modify Player class!
class Player:
    due = 200
    income = 0
    tax_rate = 0.2
    handling_fee_rate = 0
    prison_rounds = 2

    def __init__(self, name):
        self.name = name
        self.money = 100000
        self.position = 0
        self.num_rounds_in_jail = 0

    def updateAsset(self):
        self.money += Player.income

    def payDue(self):
        self.money += Player.income * (1 - Player.tax_rate)
        self.money -= Player.due * (1 + Player.handling_fee_rate)

    def printAsset(self):
        print("Player %s's money: %d" % (self.name, self.money))

    def putToJail(self):
        self.num_rounds_in_jail = Player.prison_rounds

    def move(self, step):
        if self.num_rounds_in_jail > 0:
            self.num_rounds_in_jail -= 1
        else:
            self.position = (self.position + step) % 36



class Bank:
    def __init__(self):
        pass

    def print(self):
        print("Bank ", end='')

    def stepOn(self):
        print("You received $2,000 from the Bank!")
        receiveMoney(2000, 0)

class Jail:
    def __init__(self):
        pass

    def print(self):
        print("Jail ", end='')

    def stepOn(self):
        choice = None
        while choice != "y" and choice != "n":
            choice = input("Pay $1000 to reduce the prison round to 1? [y/n]\n")
            if choice == "y":
                if haveEnoughBalance(1000, 0.1):
                    cur_player.prison_rounds = 1
                    pay(1000, 0.1)
                else:
                    print("You do not have enough money!")
                    choice = None
            elif choice == "n":
                cur_player.prison_rounds = 2

        cur_player.putToJail()


class Land:
    land_price = 1000
    upgrade_fee = [1000, 2000, 5000]
    toll = [500, 1000, 1500, 4000]
    tax_rate = [0.1, 0.15, 0.2, 0.25]

    def __init__(self):
        self.owner = None
        self.level = 0

    def print(self):
        if self.owner is None:
            print("Land ", end='')
        else:
            print("%s:Lv%d" % (self.owner.name, self.level), end="")
    
    def buyLand(self):
        if haveEnoughBalance(land_price, 0.1):
            self.owner = cur_player
            pay(land_price, 0.1)
        else:
            print("You do not have enough money to buy the land!")
    
    def upgradeHouse(self):
        upgradeFee = self.upgrade_fee[self.level]
        if haveEnoughBalance(upgradeFee, 0.1):
            pay(upgradeFee, 0.1);
            self.level += 1
        else:
            print("You do not have enough money to upgrade the land!")
    
    def chargeToll(self):
        toll = self.toll[self.level]
        taxRate = self.tax_rate[self.level]
        toll = min(toll, cur_player.money)
        pay(toll, 0)
        receiveMoney(toll, taxRate, self.owner)
        self.owner.payDue()

    def stepOn(self):
        choice = None
        if self.owner == None:
            while choice != "y" and choice != "n":
                choice = input("Pay ${} to buy the land? [y/n]\n".format(self.land_price))
                if choice == "y":
                    self.upgradeHouse()
        elif self.owner == cur_player:
            try:
                upgradeFee = self.upgrade_fee[self.level]
            except:
                return
            while choice != "y" and choice != "n":
                choice = input("Pay ${} to upgrade the land? [y/n]\n".format(upgradeFee))
                if choice == "y":
                    self.upgradeHouse()
        else:
            print("You need to pay player {} ${}".format(self.owner, self.toll[self.level]))



players = [Player("A"), Player("B")]
cur_player = players[0]
num_players = len(players)
cur_player_idx = 0
cur_player = players[cur_player_idx]
num_dices = 1
cur_round = 0
max_round = 100

game_board = [
    Bank(), Land(), Land(), Land(), Land(), Land(), Land(), Land(), Land(), Jail(),
    Land(), Land(), Land(), Land(), Land(), Land(), Land(), Land(),
    Jail(), Land(), Land(), Land(), Land(), Land(), Land(), Land(), Land(), Jail(),
    Land(), Land(), Land(), Land(), Land(), Land(), Land(), Land()
]
game_board_size = len(game_board)


def printCellPrefix(position):
    occupying = []
    for player in players:
        if player.position == position and player.money > 0:
            occupying.append(player.name)
    print(" " * (num_players - len(occupying)) + "".join(occupying), end='')
    if len(occupying) > 0:
        print("|", end='')
    else:
        print(" ", end='')


def printGameBoard():
    print("-" * (10 * (num_players + 6)))
    for i in range(10):
        printCellPrefix(i)
        game_board[i].print()
    print("\n")
    for i in range(8):
        printCellPrefix(game_board_size - i - 1)
        game_board[-i - 1].print()
        print(" " * (8 * (num_players + 6)), end="")
        printCellPrefix(i + 10)
        game_board[i + 10].print()
        print("\n")
    for i in range(10):
        printCellPrefix(27 - i)
        game_board[27 - i].print()
    print("")
    print("-" * (10 * (num_players + 6)))


def termination_check():

    # ...

    return True


def throwDice():
    step = 0
    for i in range(num_dices):
        step += random.randint(1, 6)
    return step


def main():
    global cur_player
    global num_dices
    global cur_round
    global cur_player_idx

    while termination_check():
        printGameBoard()
        for player in players:
            player.printAsset()

    # ...

# Custom methods below

# Check if a player has enough money to pay the fee
def haveEnoughBalance(amount, feeRate, player=cur_player):
    total = amount * (1 + feeRate)
    return player.money >= total

# Pay the fee for a player
def pay(amount, feeRate, player=cur_player):
    player.due = amount
    player.handling_fee_rate = feeRate
    player.payDue()
    player.due = 0

# Send money to a player
def receiveMoney(amount, taxRate, player=cur_player):
    player.income = amount
    player.tax_rate = taxRate
    player.payDue()
    player.income = 0

if __name__ == '__main__':
    main()
