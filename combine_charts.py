from PIL import Image, ImageDraw, ImageFont

# Paths to your four images
paths = [
    "plots/daily/photosyntheticallyActiveRadiation/2025-06-10.png",
    "plots/daily/temperature/2025-06-10.png",
    "plots/daily/vaporPressureDeficit/2025-06-10.png",
    "plots/daily/humidity/2025-06-10.png",
]

# Labels to add to each subplot
labels = ["A", "B", "C", "D"]

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

# Prepare for drawing
draw = ImageDraw.Draw(combined)
try:
    # Use a truetype font if available (for better rendering)
    font = ImageFont.truetype("arial.ttf", size=36)
except:
    # Fall back to default font
    font = ImageFont.load_default()

# Coordinates for where each image and label goes
positions = [
    (0, 0),                      # A
    (max_width, 0),              # B
    (0, max_height),             # C
    (max_width, max_height)      # D
]

# Paste images and draw corresponding label
for img, label, pos in zip(images, labels, positions):
    combined.paste(img, pos)

    # Position for the label (slightly offset from top-left)
    label_x = pos[0] + 10
    label_y = pos[1] + 10
    draw.text((label_x, label_y), label, fill="black", font=font)

# Save result
combined.save("plots/daily/combined_2x2_labeled.png")



from PIL import Image, ImageDraw, ImageFont

# Paths to your four images
paths = [
    "plots/monthly/photosyntheticallyActiveRadiation/2025-06.png",
    "plots/monthly/temperature/2025-06.png",
    "plots/monthly/vaporPressureDeficit/2025-06.png",
    "plots/monthly/humidity/2025-06.png",
]

# Labels for each subplot
labels = ["A", "B", "C", "D"]

# Open all images
images = [Image.open(p) for p in paths]

# Resize to same dimensions
widths, heights = zip(*(img.size for img in images))
max_width = max(widths)
max_height = max(heights)
images = [img.resize((max_width, max_height)) for img in images]

# Create blank canvas
grid_width = max_width * 2
grid_height = max_height * 2
combined = Image.new("RGB", (grid_width, grid_height), (255, 255, 255))

# Prepare drawing context
draw = ImageDraw.Draw(combined)
try:
    font = ImageFont.truetype("arial.ttf", size=36)
except:
    font = ImageFont.load_default()

# Positions for images and labels
positions = [
    (0, 0),                      # A
    (max_width, 0),              # B
    (0, max_height),             # C
    (max_width, max_height)      # D
]

# Paste images and draw labels
for img, label, pos in zip(images, labels, positions):
    combined.paste(img, pos)
    label_pos = (pos[0] + 10, pos[1] + 10)
    draw.text(label_pos, label, fill="black", font=font)

# Save the final combined image
combined.save("plots/monthly/combined_2x2_labeled.png")

