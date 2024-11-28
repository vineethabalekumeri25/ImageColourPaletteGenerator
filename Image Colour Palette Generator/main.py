from flask import Flask, request, render_template
from PIL import Image
import numpy as np
from collections import Counter
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def get_dominant_colors(image_path, num_colors=10):
    image = Image.open(image_path)
    image = image.resize((150, 150))  # Resize for faster processing
    image_array = np.array(image)
    pixels = image_array.reshape(-1, 3)
    color_counts = Counter(map(tuple, pixels))
    total_pixels = sum(color_counts.values())

    # Get the most common colors
    most_common_colors = color_counts.most_common(num_colors)

    # Calculate percentages
    color_data = []
    for (r, g, b), count in most_common_colors:
        hex_color = '#{:02x}{:02x}{:02x}'.format(r, g, b)
        percentage = (count / total_pixels) * 100
        color_data.append({'color': hex_color, 'count': count, 'percentage': percentage})

    return color_data


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Handle file upload
        if 'image' not in request.files:
            return "No file uploaded."

        file = request.files['image']
        if file.filename == '':
            return "No selected file."

        # Save the uploaded file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Extract dominant colors
        color_data = get_dominant_colors(filepath)
        color_count = len(color_data)  # Total number of colors detected (should be 10)

        return render_template("result.html", color_data=color_data, color_count=color_count, image_url=filepath)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)