from flask import Flask, request, jsonify, render_template
import pyfiglet
from PIL import Image
import numpy as np
import io

app = Flask(__name__)

# ASCII characters for image conversion
ASCII_CHARS = "@%#*+=-:. "

def image_to_ascii(image_path, width=100):
    """Convert an image to ASCII art."""
    img = Image.open(image_path).convert('L')  # Convert to grayscale
    w, h = img.size
    aspect_ratio = h / w
    new_height = int(width * aspect_ratio * 0.55)
    img = img.resize((width, new_height))
    pixels = np.array(img)
    ascii_str = ""
    for row in pixels:
        for pixel in row:
            ascii_str += ASCII_CHARS[pixel // 25]
        ascii_str += "\n"
    return ascii_str

def text_to_ascii(text, font):
    """Convert text to ASCII art using a specific font."""
    try:
        return pyfiglet.figlet_format(text, font=font)
    except pyfiglet.FontNotFound:
        return "Font not found."

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_ascii():
    """Generate ASCII art based on user input."""
    if 'image' in request.files:
        # Handle image upload
        file = request.files['image']
        ascii_art = image_to_ascii(file)
        return ascii_art
    else:
        # Handle text input
        data = request.get_json()
        text = data.get('text', '')
        font = data.get('font', 'standard')
        ascii_art = text_to_ascii(text, font)
        return ascii_art

@app.route('/fonts', methods=['GET'])
def get_fonts():
    """Return a list of available fonts for text-to-ASCII conversion."""
    figlet = pyfiglet.Figlet()  # Create a Figlet instance
    fonts = figlet.getFonts()   # Call getFonts() on the Figlet instance
    return jsonify(sorted(fonts))  # Return the list of fonts in JSON format

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)  # Bind to all IPs

