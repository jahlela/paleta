import itertools

from image_analysis import get_display_colors



top_bin_colors = [(154995, (19, 255, 237)), (125281, (23, 255, 242)), (52067, (0, 255, 113)), (2816, (31, 255, 236)), (1878, (254, 255, 126)), (180, (56, 145, 114))]


display_colors = get_display_colors(top_bin_colors, 35, 20000)






def find_distinct_colors(display_colors):
    """ Takes in a list of hex colors and """

    print 'display_colors', display_colors

    
    

    # Convert hex to decimal for percent difference
    for color in display_colors:
        dec_colors = [int(x[1:], 16) for x in display_colors]
    
    dec_colors.sort()
    print 'dec_colors', dec_colors

    # diff_interval is maximum possible value (white:FFFFFF:16777215) / 100, 
    # rounded down to nearest 10 --> 167770
    diff_interval = 167770

    next_min = dec_colors[0] + diff_interval
    keepers = []

    for color in dec_colors:
        # If the color is different enough, add it to keepers and update next_min
        if next_min =< color:
            print 'color', color
            hex_color = "#" + hex(color)[2:]
            keepers.append(hex_color)
            next_min = color + diff_interval
        print color, next_min
    
    print 'keepers', keepers
    return keepers
        
find_distinct_colors(display_colors)



