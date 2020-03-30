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
        print("You received $2000 from the Bank!")
        receiveMoney(2000, 0, cur_player)

        return


class Jail:
    def __init__(self):
        pass

    def print(self):
        print("Jail ", end='')

    def stepOn(self):
        if cur_player.num_rounds_in_jail > 0:
            return
        choice = None
        while choice != "y" and choice != "n":
            choice = input("Pay $1000 to reduce the prison round to 1? [y/n]\n")
            if choice == "y":
                if haveEnoughBalance(1000, 0.1, cur_player):
                    Player.prison_rounds = 1
                    pay(1000, 0.1, cur_player)
                else:
                    print("You do not have enough money to reduce the prison round!")
                    choice = None
            elif choice == "n":
                Player.prison_rounds = 2

        cur_player.putToJail()


class Land:
    land_price = 1000
    upgrade_fee = [1000, 2000, 5000]
    toll = [500, 1000, 1500, 3000]
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
        if haveEnoughBalance(self.land_price, 0.1, cur_player):
            self.owner = cur_player
            pay(self.land_price, 0.1, cur_player)
        else:
            print("You do not have enough money to buy the land!")

        cur_player.payDue()
    
    def upgradeLand(self):
        upgradeFee = self.upgrade_fee[self.level]
        if haveEnoughBalance(upgradeFee, 0.1, cur_player):
            pay(upgradeFee, 0.1, cur_player)
            self.level += 1
        else:
            print("You do not have enough money to upgrade the land!")

        cur_player.payDue()
    
    def chargeToll(self):
        toll = self.toll[self.level]
        taxRate = self.tax_rate[self.level]
        toll = min(toll, cur_player.money)
        pay(toll, 0, cur_player)
        cur_player.payDue()
        receiveMoney(toll, taxRate, self.owner)
        self.owner.payDue()

    def stepOn(self):
        choice = None
        if self.owner is None:
            while choice != "y" and choice != "n":
                choice = input("Pay ${} to buy the land? [y/n]\n".format(self.land_price))
                if choice == "y":
                    self.buyLand()
        elif self.owner == cur_player:
            try:
                upgradeFee = self.upgrade_fee[self.level]
            except:
                return
            while choice != "y" and choice != "n":
                choice = input("Pay ${} to upgrade the land? [y/n]\n".format(upgradeFee))
                if choice == "y":
                    self.upgradeLand()
        else:
            print("You need to pay player {} ${}".format(self.owner.name, self.toll[self.level]))
            self.chargeToll()

        return



players = [Player("A"), Player("B")]
cur_player = players[0]
num_players = len(players)
cur_player_idx = 0
cur_player = players[cur_player_idx]
num_dices = 1
cur_round = 0

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


def terminationCheck():
    if players[0].money == 0 or players[1].money == 0:
        return False
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

    while terminationCheck():
        printGameBoard()
        for player in players:
            player.printAsset()

        cur_player_idx = cur_round % 2
        cur_player = players[cur_player_idx]

        # Display game information
        print("Player {}'s turn.".format(cur_player.name))

        # If in Jail
        if cur_player.num_rounds_in_jail > 0:
            pay(200, 0, cur_player)  # Still need to pay the fixed cost
            cur_player.move(0)
            cur_round += 1
            print("Player {} is in jail.".format(cur_player.name))
            continue

        # Fixed cost of each round
        pay(200, 0, cur_player)

        # Ask if player wants to throws two dice
        choice = None
        while choice != "y" and choice != "n":
            choice = input("Pay $500 to throw two dice? [y/n]\n")
            if choice == "y":
                if haveEnoughBalance(500, 0.05, cur_player):
                    num_dices = 2
                    pay(500, 0.05, cur_player)
                else:
                    print("You do not have enough money to throw two dice!")
            elif choice == "n":
                num_dices = 1

        # Throw the dice
        points_of_dice = throwDice()
        print("Points of dice: {}".format(points_of_dice))
        cur_player.move(points_of_dice)
        pos = cur_player.position
        game_board[pos].stepOn()
        cur_round += 1

    winner = players[cur_round % 2]
    print("Game over! winner: {}.".format(winner.name))

# Custom methods below


# Check if a player has enough money to pay the fee
def haveEnoughBalance(amount, fee_rate, player):
    total = amount * (1 + fee_rate)
    return player.money >= total


# Pay the fee for a player
def pay(amount, fee_rate, player):
    Player.due = min(player.money, amount)
    Player.handling_fee_rate = fee_rate
    player.payDue()
    Player.due = 0


# Send money to a player
def receiveMoney(amount, tax_rate, player):
    Player.income = amount
    Player.tax_rate = tax_rate
    player.payDue()
    Player.income = 0


if __name__ == '__main__':
    main()
