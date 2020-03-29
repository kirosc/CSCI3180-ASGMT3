use strict;
use warnings;
use List::MoreUtils 'first_index';

package Game;
use MannerDeckStudent; 
use Player;

sub new {
  my $class = shift;
  my $self = {
    _deck => shift,
    _player => [],
    _cards => [],
  };
  return bless $self, $class;
}

sub setPlayers {
  my ( $self, $players_name ) = @_;
  my $numberOfPlayers = 0+@{$players_name};
  # Cards can't be divided evenly
  if (52 % $numberOfPlayers != 0) {
    print "Error: cards' number 52 can not be divided by players number ${numberOfPlayers}!\n";
    return 0;
  }

  for my $name (@{$players_name}) {
    my $_player = new Player($name);
    push @{$self->{_player}}, $_player;
  }
  return 1;
}

sub getReturn {
  my $self = shift;
  my $cards = $self->{_cards};
  my $card = @{$cards}[-1];
  my $size = 0+@{$cards};

  if ($card eq "J" && $size != 1) {
    return $size;
  } elsif ($size == 1) {
    return 0;
  } else {
    my $match_idx = $size;
    for (my $i = 0; $i < @{$cards} && $i < $size - 1; $i++) {
      my $current_card = @{$cards}[$i];
      if ($current_card eq $card) {
        $match_idx = $i;
        last;
      }
    }
    return $size - $match_idx;
  }
}

sub numCards {
  my $self = shift;
  return 0+@{$self->{_cards}};
}

sub showCards {
  my $self = shift;
  print join (" ", @{$self->{_cards}})."\n";
}

sub startGame {
  my $self = shift;
  my $players = $self->{_player};
  print join "", "There ", 0+@{$players},  " players in the game:\n";
  my $deck = new MannerDeckStudent();
  $deck->shuffle();
  my @setOfCards = $deck->AveDealCards(2);
  # Distribute cards
  for my $player (@{$players}) {
    print $player->{_name}." ";
    $player->{_cards} = shift @setOfCards;
  }
  print "\n\nGame begin!!!";
  
  my $round = 1;
  for (my $i = 0; 0+@{$players} > 1; $i++) {
    # Passed the last player. Reset counter.
    if ($i == 0+@{$players}) {
      $i = 0;
      $round++;
    }

    my $current_player = @{$players}[$i];
    $self->deal($current_player);

    # Player lose. Remove that player and check if someone wins.
    if ($self->check_lose($current_player)) {
      splice(@{$players}, $i--, 1);
      if (0+@{$players} == 1) {
        print join " ", "\nWinner is", @{$players}[0]->{_name}, "in game", $round."\n";
      }
    }
  }
}

sub deal {
  my ( $self, $player ) = @_;
  my $name = $player->{_name};
  my $cards = $player->{_cards};
  my $stack = $self->{_cards};

  print join "", "\n\nPlayer ", $name, " has ", 0+@{$cards}, " cards before deal.\n";
  print "=====Before player's deal=======\n";
  $self->showCards();
  print "================================\n";
  push @{$stack}, $player->dealCards();
  print join " ", $name, "==>", "card", @{$stack}[-1]."\n";
  my $returnNums = $self->getReturn();
  for (my $i = 0+@{$stack}; $returnNums != 0; $i--, $returnNums--) {
    push @{${cards}}, pop @{$stack};
  }
  print "=====After player's deal=======\n";
  $self->showCards();
  print "================================\n";
  print join "", "Player ", $name, " has ", 0+@{$cards}, " cards after deal.";
}

sub check_lose {
  my ( $self, $player ) = @_;
  my $name = $player->{_name};
  my $cards = $player->{_cards};

  if (0+@{$cards} == 0) {
    print join "", "\nPlayer ", $name, " has no cards, out!\n";
    return 1;
  }
  return 0;
}

return 1;