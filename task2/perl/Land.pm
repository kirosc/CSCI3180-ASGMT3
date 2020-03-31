use strict;
use warnings;
use List::Util qw[min];
package Land;

our @upgrade_fee = (1000, 2000, 5000);
our @toll = (500, 1000, 1500, 3000);
our @tax_rate = (0.1, 0.15, 0.2, 0.25);

sub new {
    my $class = shift;
    my $self  = {
        owner => undef,
        level => 0,
    };
    bless $self, $class;
    return $self;
}

sub print {
    my $self = shift;
    if (!defined($self->{owner})) {
        print("Land ");
    } else {
        print("$self->{owner}->{name}:Lv$self->{level}");
    }
}

sub buyLand {
    my $self = shift;
    if ($main::cur_player->haveEnoughBalance(1000, 0.1)) {
        local $Player::due = 1000;
        local $Player::handling_fee_rate = 0.1;
        $main::cur_player->payDue();
        $self->{owner} = $main::cur_player;
    } else {
        print("You do not have enough money to buy the land!");
    }

    $main::cur_player->payDue();
}

sub upgradeLand {
    my $self = shift;
    local $Player::due = $upgrade_fee[$self->{level}];
    local $Player::handling_fee_rate = 0.1;
    if ($main::cur_player->haveEnoughBalance($Player::due, $Player::handling_fee_rate)) {
        $self->{level}++;
    } else {
        print("You do not have enough money to upgrade the land!");
    }

    $main::cur_player->payDue();
}

sub chargeToll {
    my $self = shift;
    local $Player::due = $toll[$self->{level}];
    $Player::due = min($Player::due, $main::cur_player->{money});
    $main::cur_player->payDue();

    $Player::due = 0;
    local $Player::income = $Player::due;
    local $Player::tax_rate = $Player::tax_rate[$self->{level}];
    $self->{owner}->payDue();
}

sub stepOn {
    my $self = shift;
    my $choice = "";

    if (!defined $self->{owner}) {
        while ($choice ne "y" && $choice ne "n") {
            $choice = <STDIN>;
            chomp $choice;
            print ("Pay \$1000 to buy the land? [y/n]\n");
            if ($choice eq "y") {
                $self->buyLand();
            }
        }
    } elsif ($self->{owner} == $main::cur_player) {
        if ($self->{level} == 3) {
            return;
        }
        while ($choice ne "y" && $choice ne "n") {
            $choice = <STDIN>;
            chomp $choice;
            print ("Pay $upgrade_fee[$self->{level}] to upgrade the land? [y/n]\n");
            if ($choice eq "y") {
                $self->upgradeLand();
            }
        }
    } else {
        print ("You need to pay player $self->{owner}->{name} $toll[$self->{level}]");
        $self->chargeToll();
    }
}
1;