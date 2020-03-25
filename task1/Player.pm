use strict;
use warnings;
 
package Player;
sub new {
  my $class = shift;
  my $self = {
    _name => shift,
    _cards => [],
  }
}

sub getCards {
  my ( $self, $card ) = @_;
  push @{$self->{_cards}}, card;
  return @{$self->{_cards}}[-1];
}

sub dealCards {
  my $self = shift;
  return shift @{$self->{_cards}};
}

sub numCards {
  my $self = shift;
  return 0+@{$self->{_cards}};
}

return 1;