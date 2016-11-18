










# def add_color_bins_to_db(self):
#         """ Takes an image_id, calculates and adds its color bins to the db """

#         bins = self.get_image_color_bins()

#         for color_bin in bins:
#             # bin_for_image = ImageColorBin.query.filter(image_id==self.image_id, 
#                                                         # color_bin==color_bin)

#             if not bin_for_image:
#                 new_image_color_bin = ImageColorBin(image_id=image_id, color_bin=color_bin)
#                 db.session.add(new_image_color_bin)
#                 db.session.commit()

#         return

# # Add db image object as parameter
# def get_image_color_bins(self):
#     """ takes an image_id, and loops through its colors, creating 
#         a set of the base-4 codes for each bin represented by that image,
#         then commits a record for each bin associated with the image to the db """
    
#     # Grab colors from image 
#     color_string = self.colors
#     colors = color_string.split(",")

#     # Will hold a list of bins to associate with this image
#     bins = []

#     # Calculate the bin for each 
#     for color in colors:
#         hex_color = color[1:]
#         rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (0, 2 ,4))

#         bin = ''
#         # Grab values for red, green, blue channels and round down to the 
#         # nearest 64 and divide by 64 to find bin 
#         for channel in rgb_color:
#             bin_partial = (channel - (channel % 64))/64
#             bin += str(bin_partial)

#         bins.append(bin)

#     return bins





