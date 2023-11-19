# WebArtPainter

WebArtPainter is a Python program that allows you to create artistic images directly on websites. With the ability to customize your color palette using RGB codes, you can bring your creative vision to life effortlessly.

## Features:

- **Web-based Art Creation**: Generate impressive artwork directly on websites with ease.

- **Customizable Color Palette**: Tailor your color choices by inputting RGB codes, enabling the creation of unique and vibrant images.

- **Interruptible Process**: Press `Esc` at any time to gracefully exit the program.

- **Image Input**: The program requires an image for drawing. Use the following example code to set the image:

```python
from paint import Paint

# Create an instance of Paint
tracker = Paint()

# Change the image for drawing
tracker.change_image("image.png")

# Start the calibration process
tracker.start_calibration()

# Draw the image on the website
tracker.drawImage()
