
from PIL import Image, ImageFilter

# Load images and convert them to ensure compatibility
im_leads = Image.open('colormask_example.png').convert('RGBA')
im_back = Image.open('background_example.png').convert('RGBA')

# Create a mask based on im_leads white pixels
# Pixels that were white in im_leads are now transparent in the mask (0),
# and all other pixels are opaque (255).
mask = im_leads.point(lambda p: 0 if p == 255 else 255).convert('L')

# Create a black image of the same size as im_leads and im_back
im_black = Image.new('RGBA', im_leads.size, (55, 55, 55, 100))

# Use the mask to determine which parts of the black image and im_back to show:
# Where mask is opaque (255), im_black will be used.
# Where mask is transparent (0), im_back will show through.
result_image = Image.composite(im_black, im_back, mask)

# Save the result
result_image.save("join_back_leads.png")


blurred_image = result_image.filter(ImageFilter.GaussianBlur(radius=2))  # Adjust radius as needed

# Save the blurred result
blurred_image.save("blurred_join_back_leads.png")



