from PIL import Image

# Paths to your four images
paths = [
    "plots/daily/photosyntheticallyActiveRadiation/2025-06-10.png",
    "plots/daily/temperature/2025-06-10.png",
    "plots/daily/vaporPressureDeficit/2025-06-10.png",
    "plots/daily/humidity/2025-06-10.png",
]

# Open all images
images = [Image.open(p) for p in paths]

# Optionally resize to same size (if not already the same)
widths, heights = zip(*(img.size for img in images))
max_width = max(widths)
max_height = max(heights)

# Resize images to the same size
images = [img.resize((max_width, max_height)) for img in images]

# Create a new blank canvas for 2x2 grid
grid_width = max_width * 2
grid_height = max_height * 2
combined = Image.new("RGB", (grid_width, grid_height), (255, 255, 255))

# Paste images into the grid
combined.paste(images[0], (0, 0))
combined.paste(images[1], (max_width, 0))
combined.paste(images[2], (0, max_height))
combined.paste(images[3], (max_width, max_height))

# Save result
combined.save("plots/daily/combined_2x2.png")


from PIL import Image

# Paths to your four images
paths = [
    "plots/monthly/photosyntheticallyActiveRadiation/2025-06.png",
    "plots/monthly/temperature_daytime/2025-06.png",
    "plots/monthly/vaporPressureDeficit/2025-06.png",
    "plots/monthly/humidity/2025-06.png",
]

# Open all images
images = [Image.open(p) for p in paths]

# Optionally resize to same size (if not already the same)
widths, heights = zip(*(img.size for img in images))
max_width = max(widths)
max_height = max(heights)

# Resize images to the same size
images = [img.resize((max_width, max_height)) for img in images]

# Create a new blank canvas for 2x2 grid
grid_width = max_width * 2
grid_height = max_height * 2
combined = Image.new("RGB", (grid_width, grid_height), (255, 255, 255))

# Paste images into the grid
combined.paste(images[0], (0, 0))
combined.paste(images[1], (max_width, 0))
combined.paste(images[2], (0, max_height))
combined.paste(images[3], (max_width, max_height))

# Save result
combined.save("plots/monthly/combined_2x2.png")
