#!/usr/bin/env python
#
# Card level-up requirements (EXP) calculator

import os
import sys
import getopt

# The EXP tables
# data from: http://www59.atwiki.jp/lovelive-sif/pages/32.html
# these have -1 as the first value because python arrays are 0-based and I am using <level> as the index
# and am too lazy to do <level-1> to account for the 0-based-ness :P
exp_table_n = [-1, 0, 6, 18, 28, 40, 51, 61, 72, 82, 93, 104, 114, 124, 135, 145, 156, 165, 176, 187, 196, 207, 217, 226, 238, 247, 257, 268, 277, 288, 297, 308, 317, 328, 337, 348, 358, 367, 377, 388, 397]
exp_table_r = [-1, 0, 14, 31, 45, 55, 67, 76, 85, 94, 103, 110, 119, 125, 134, 140, 148, 155, 161, 168, 174, 181, 187, 193, 199, 206, 211, 217, 223, 228, 235, 240, 245, 251, 256, 262, 267, 272, 277, 283, 288, 292, 298, 303, 308, 313, 317, 323, 327, 332, 337, 342, 346, 351, 356, 360, 365, 370, 374, 378, 383]
exp_table_sr = [-1, 0, 54, 98, 127, 150, 169, 187, 203, 218, 232, 245, 257, 269, 281, 291, 302, 311, 322, 331, 340, 349, 358, 366, 374, 383, 391, 398, 406, 413, 421, 428, 435, 442, 449, 456, 462, 469, 475, 482, 488, 494, 500, 507, 512, 518, 524, 530, 536, 541, 547, 552, 558, 563, 568, 574, 579, 584, 590, 594, 600, 605, 609, 615, 619, 625, 629, 634, 639, 643, 648, 653, 657, 662, 667, 670, 676, 680, 684, 689, 693]
exp_table_ur = [-1, 0, 201, 294, 345, 382, 411, 438, 460, 481, 499, 517, 532, 547, 561, 574, 587, 598, 611, 621, 631, 642, 651, 661, 670, 679, 687, 696, 704, 712, 720, 727, 734, 742, 749, 755, 763, 769, 775, 782, 788, 794, 800, 806, 812, 818, 823, 829, 834, 840, 845, 850, 856, 860, 866, 870, 875, 880, 885, 890, 894, 899, 903, 908, 912, 917, 921, 925, 930, 933, 938, 942, 946, 950, 954, 959, 961, 966, 970, 974, 977, 981, 985, 988, 992, 996, 999, 1003, 1006, 1010, 1013, 1017, 1020, 1024, 1027, 1030, 1034, 1037, 1040, 1043, 1047]

# max levels
# note we don't check whether the card is idolized or not
# we assume that the user knows what they're doing
level_cap_n = 40
level_cap_r = 60
level_cap_sr = 80
level_cap_ur = 100

def check_level_cap(rarity, level):
    return_value = False
    if level >= 1:
        if rarity == "N":
            return_value = (level <= level_cap_n)
        elif rarity == "R":
            return_value = (level <= level_cap_r)
        elif rarity == "SR":
            return_value = (level <= level_cap_sr)
        elif rarity == "UR":
            return_value = (level <= level_cap_ur)
    return return_value

def check_valid_exp(rarity, level, exp):
    return_value = False
    if rarity == "N" and check_level_cap(rarity, level):
        return_value = (exp >= 0 and exp < exp_table_n[level])
    elif rarity == "R" and check_level_cap(rarity, level):
        return_value = (exp >= 0 and exp < exp_table_r[level])
    elif rarity == "SR" and check_level_cap(rarity, level):
        return_value = (exp >= 0 and exp < exp_table_sr[level])
    elif rarity == "UR" and check_level_cap(rarity, level):
        return_value = (exp >= 0 and exp < exp_table_ur[level])
    return return_value

def calc(rarity, starting_level, starting_exp, desired_level):
    # assumes that all values fed into it have been checked already
    required_exp = 0
    # desired_level+1 because python ranges are not inclusive :P
    for level in range(starting_level+1, desired_level+1):
        if rarity == "N":
            required_exp = required_exp + exp_table_n[level]
        elif rarity == "R":
            required_exp = required_exp + exp_table_r[level]
        elif rarity == "SR":
            required_exp = required_exp + exp_table_sr[level]
        elif rarity == "UR":
            required_exp = required_exp + exp_table_ur[level]
        #print "WE ARE AT LEVEL %d and we need %d exp" % (level, required_exp)
    # subtract what we already have
    required_exp = required_exp - starting_exp
    # now tell the user
    print "To get a %s card from level %d (with %d EXP) to %d requires %d EXP." % (rarity, starting_level, starting_exp, desired_level, required_exp)
    # calculate equivalent N cards (round up because we can't feed half of a card)
    number_of_n_cards = (required_exp // 100) + 1
    print "(the equivalent of about %d level-1 N cards fed to it)" % number_of_n_cards

def usage():
    print "Usage: %s [options]" % os.path.basename(__file__)
    print "where [options] can be one or more of:"
    print "[-H | --help]            Print this help message"
    print "[-r | --rarity]          Card's rarity (REQUIRED, must be one of: N, R, SR, UR)"
    print "[-l | --starting-level]  Card's starting level (REQUIRED)"
    print "[-e | --starting-exp]    Card's starting EXP (optional, defaults to 0)"
    print "[-L | --desired-level]   Card's desired level (optional, defaults to max level)"

def main(argv):
    rarity = None
    starting_level = None
    desired_level = None
    starting_exp = 0
    try:                                
        options, remainder = getopt.getopt(argv, "Hr:l:e:L:", ["help", "rarity=", "starting-level=", "starting-exp=", "desired-level="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)                     
    for opt, arg in options:
        if opt in ('-H', '--help'):
            usage()
            sys.exit(0)
        elif opt in ('-r', '--rarity'):
            rarity = arg
        elif opt in ('-l', '--starting-level'):
            starting_level = int(arg)
        elif opt in ('-e', '--starting-exp'):
            starting_exp = int(arg)
        elif opt in ('-L', '--desired-level'):
            desired_level = int(arg)

    # first validate rarity
    if rarity is None:
        print "Error: must specify rarity"
        usage()
        sys.exit(1)
    else:
        # canonicalize it to uppercase
        rarity = rarity.upper()
        if rarity != "N" and rarity != "R" and rarity != "SR" and rarity != "UR":
            print "Error: invalid rarity specified (%s)" % rarity
            usage()
            sys.exit(1)

    # now validate starting level
    if starting_level is None:
        print "Error: must specify starting level"
        usage()
        sys.exit(1)
    elif not check_level_cap(rarity, starting_level):
        print "Error: invalid starting level: %d" % starting_level
        usage()
        sys.exit(1)

    # now validate starting level
    if desired_level is None:
        if rarity == "N":
            desired_level = level_cap_n
        elif rarity == "R":
            desired_level = level_cap_r
        elif rarity == "SR":
            desired_level = level_cap_sr
        elif rarity == "UR":
            desired_level = level_cap_ur
    elif not check_level_cap(rarity, desired_level):
        print "Error: invalid desired level: %d" % desired_level
        usage()
        sys.exit(1)
        
    # now do start+desired levels make sense?
    if desired_level <= starting_level:
        print "Error: desired level must be greater than starting level"
        usage()
        sys.exit(1)
    
    # finally check to see if exp makes sense (can't be >= the number of exp for the next level)
    if not check_valid_exp(rarity, desired_level, starting_exp):
        print "Error: invalid EXP (%d)" % starting_exp
        usage()
        sys.exit(1)
        
    # all is well, go for it
    calc(rarity, starting_level, starting_exp, desired_level)

### main script starts here

if __name__ == "__main__":
    main(sys.argv[1:])