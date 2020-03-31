use strict;
use warnings;
require "./Player.pm";

package Jail;
sub new {
    my $class = shift;
    my $self  = {};
    bless $self, $class;
    return $self;
}

sub print {
    print("Jail ");
}

sub stepOn {
    if ($main::cur_playe->{num_rounds_in_jail} > 0) {
        return;
    }
    
    my $choice = "";
    while ($choice ne "y" && $choice ne "n") {
        $choice = <STDIN>;
        chomp $choice;
        if ($choice eq "y") {
            if ($main::cur_player->haveEnoughBalance(1000, 0.1)) {
                local $Player::prison_rounds = 1;
                local $Player::due = 1000;
                local $Player::handling_fee_rate = 0.1;
                $main::cur_player->payDue();
            }
        } elsif ($choice eq "n") {
            local $Player::prison_rounds = 2;
        }
    }

    $main::cur_player->putToJail();
}

1;
