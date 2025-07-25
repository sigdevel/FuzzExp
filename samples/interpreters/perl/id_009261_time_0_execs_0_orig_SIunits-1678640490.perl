package main;
sub do_cmd_yocto { "y" . $_[0] }
sub do_cmd_zepto { "z" . $_[0] }
sub do_cmd_atto { "a" . $_[0] }
sub do_cmd_femto { "f" . $_[0] }
sub do_cmd_pico { "p" . $_[0] }
sub do_cmd_nano { "n" . $_[0] }
sub do_cmd_milli { "m" . $_[0] }
sub do_cmd_centi { "c" . $_[0] }
sub do_cmd_deci { "d" . $_[0] }
sub do_cmd_deca { "da" . $_[0] }
sub do_cmd_hecto { "h" . $_[0] }
sub do_cmd_kilo { "k" . $_[0] }
sub do_cmd_mega { "M" . $_[0] }
sub do_cmd_giga { "G" . $_[0] }
sub do_cmd_tera { "T" . $_[0] }
sub do_cmd_peta { "P" . $_[0] }
sub do_cmd_exa { "E" . $_[0] }
sub do_cmd_zetta { "Z" . $_[0] }
sub do_cmd_yotta { "Y" . $_[0] }
sub do_cmd_gram { "g" . $_[0] }
sub do_cmd_metre { "m" . $_[0] }
sub do_cmd_second { "s" . $_[0] }
sub do_cmd_ampere { "A" . $_[0] }
sub do_cmd_kelvin { "K" . $_[0] }
sub do_cmd_mole { "mol" . $_[0] }
sub do_cmd_candela { "cd" . $_[0] }
sub do_cmd_radian { "rad" . $_[0] }
sub do_cmd_steradian { "sr" . $_[0] }
sub do_cmd_hertz { "Hz" . $_[0] }
sub do_cmd_newton { "N" . $_[0] }
sub do_cmd_pascal { "Pa" . $_[0] }
sub do_cmd_joule { "J" . $_[0] }
sub do_cmd_watt { "W" . $_[0] }
sub do_cmd_coulomb { "C" . $_[0] }
sub do_cmd_volt { "V" . $_[0] }
sub do_cmd_farad { "F" . $_[0] }
sub do_cmd_siemens { "S" . $_[0] }
sub do_cmd_weber { "Wb" . $_[0] }
sub do_cmd_tesla { "T" . $_[0] }
sub do_cmd_henry { "H" . $_[0] }
sub do_cmd_lumen { "lm" . $_[0] }
sub do_cmd_lux { "lx" . $_[0] }
sub do_cmd_becquerel { "Bq" . $_[0] }
sub do_cmd_sievert { "Sv" . $_[0] }
sub do_cmd_katal { "kat" . $_[0] }
sub do_cmd_minute { "min" . $_[0] }
sub do_cmd_hour { "h" . $_[0] }
sub do_cmd_dday { "d" . $_[0] }
sub do_cmd_ton { "t" . $_[0] }
sub do_cmd_tonne { "t" . $_[0] }
sub do_cmd_liter { "L" . $_[0] }
sub do_cmd_litre { "l" . $_[0] }
sub do_cmd_neper { "Np" . $_[0] }
sub do_cmd_bel { "B" . $_[0] }
sub do_cmd_curie { "Ci" . $_[0] }
sub do_cmd_rad { "rad" . $_[0] }
sub do_cmd_arad { "rd" . $_[0] }
sub do_cmd_rem { "rem" . $_[0] }
sub do_cmd_roentgen { "R" . $_[0] }
sub do_cmd_atomicmass { "u" . $_[0] }
sub do_cmd_are { "a" . $_[0] }
sub do_cmd_barn { "b" . $_[0] }
sub do_cmd_bbar { "bar" . $_[0] }
sub do_cmd_gal { "Gal" . $_[0] }
sub do_cmd_unit {
local($_) = @_;
s/$next_pair_pr_rx//o;
$quantity = $2;
s/$next_pair_pr_rx//o;
$unit = $2;
$_ = $quantity . " " . $unit . $_;
}
sub do_cmd_squared {"<SUP>2</SUP>" . $_[0];}
sub do_cmd_cubed {"<SUP>3</SUP>" . $_[0];}
sub do_cmd_fourth {"<SUP>4</SUP>" . $_[0];}
sub do_cmd_reciprocal {"<SUP>-1</SUP>" . $_[0];}
sub do_cmd_rpsquared {"<SUP>-2</SUP>" . $_[0];}
sub do_cmd_rpcubed {"<SUP>-3</SUP>" . $_[0];}
sub do_cmd_rpfourth {"<SUP>-4</SUP>" . $_[0];}
sub do_SIunits_cdot {}
sub do_SIunits_amssymb {}
sub do_SIunits_thinqspace {}
1;
