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
  }
}

sub set_players {
  my ( $self, $palyers_name ) = @_;
  for my $name (@{$players_name}) {
    $_player = new Player($name);
    push @{$self->_player}, $_player;
  }
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
  print join(" ", @{$self->_cards})."\n";
}

sub start_game {

}

return 1;