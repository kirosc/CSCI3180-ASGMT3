#! /usr/bin/perl
use warnings;
use strict;
require "./Bank.pm";
require "./Jail.pm";
require "./Land.pm";
require "./Player.pm";

our @game_board = (
    new Bank(), new Land(), new Land(), new Land(), new Land(), new Land(), new Land(), new Land(), new Land(), new Jail(),
    new Land(), new Land(), new Land(), new Land(), new Land(), new Land(), new Land(), new Land(),
    new Jail(), new Land(), new Land(), new Land(), new Land(), new Land(), new Land(), new Land(), new Land(), new Jail(),
    new Land(), new Land(), new Land(), new Land(), new Land(), new Land(), new Land(), new Land(),
);
our $game_board_size = @game_board;

our @players = (new Player("A"), new Player("B"));
our $num_players = @players;

our $cur_player_idx = 0;
our $cur_player = $players[$cur_player_idx];
our $cur_round = 0;
our $num_dices = 1;

srand(0); # don't touch

# game board printing utility. Used to show player position.
sub printCellPrefix {
    my $position = shift;
    my @occupying = ();
    foreach my $player (@players) {
        if ($player->{position} == $position && $player->{money} > 0) {
            push(@occupying, ($player->{name}));
        }
    }
    print(" " x ($num_players - scalar @occupying), @occupying);
    if (scalar @occupying) {
        print("|");
    } else {
        print(" ");
    }
}

sub printGameBoard {
    print("-"x (10 * ($num_players + 6)), "\n");
    for (my $i = 0; $i < 10; $i += 1) {
        printCellPrefix($i);
        $game_board[$i]->print();
    }
    print("\n\n");
    for (my $i = 0; $i < 8; $i += 1) {
        printCellPrefix($game_board_size - $i - 1);
        $game_board[-$i-1]->print();
        print(" "x (8 * ($num_players + 6)));
        printCellPrefix($i + 10);
        $game_board[$i+10]->print();
        print("\n\n");
    }
    for (my $i = 0; $i < 10; $i += 1) {
        printCellPrefix(27 - $i);
        $game_board[27-$i]->print();
    }
    print("\n");
    print("-"x (10 * ($num_players + 6)), "\n");
}

sub terminationCheck {
    if ($players[0]->{money} == 0 || $players[0]->{money} == 0) {
        return 0;
    }
    return 1;
}

sub throwDice {
    my $step = 0;
    for (my $i = 0; $i < $num_dices; $i += 1) {
        $step += 1 + int(rand(6));
    }
    return $step;
}

sub main {
    while (terminationCheck()){
        printGameBoard();
        foreach my $player (@players) {
            $player->printAsset();
        }

        $cur_player_idx = $cur_round % 2;
        $cur_player = $players[$cur_player_idx];

        # Display game information
        print("Player $cur_player->{name}'s turn.\n");

        # Fixed cost of each round
        # TODO: $200 or remainging balance?
        $cur_player->payDue();

        # If in Jail
        if ($cur_player->{num_rounds_in_jail} > 0) {
            $cur_player->move(0);
            $cur_round++;
            print("Player $cur_player->{name} is in jail.\n");
            next;
        }

        # Ask if player wants to throws two dice
        print("Pay \$500 to throw two dice? [y/n]\n");
        my $choice = "";
        while ($choice ne "y" && $choice ne "n") {
            $choice = <STDIN>;
            chomp $choice;
            if ($choice eq "y") {
                if ($cur_player->haveEnoughBalance(500, 0.05)) {
                    local $num_dices = 2;
                    local $Player::due = 500;
                    local $Player::handling_fee_rate = 0.05;
                    $cur_player->payDue();
                } else {
                    print("You do not have enough money to throw two dice!\n");
                }
            }
        }

        # Throw the dice
        my $points_of_dice = throwDice();
        print("Points of dice: $points_of_dice");
        $cur_player->move($points_of_dice);
        my $pos = $cur_player->{position};
        $game_board[$pos]->stepOn();
        $cur_round++;
    }
    my $winner = $players[$cur_round % 2];
    print("Game over! winner: $winner->{name}.\n");
}

main();
