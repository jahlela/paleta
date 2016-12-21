
def get_color_bin(color):
        """ Takes a hex value of form '#020451' and returns a string of that color's bin """

        hex_color = color[1:]
        if hex_color == '000':
            hex_color = '000000'
        rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (0, 2 ,4))

        color_bin = ''
        # Grab values for red, green, blue channels and round down to the 
        # nearest 64 and divide by 64 to find bin 
        for channel in rgb_color:
            bin_partial = (channel - (channel % 64))/64
            color_bin += str(bin_partial)

        return color_bin
