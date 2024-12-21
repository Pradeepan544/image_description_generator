from flask import Flask, request, jsonify, render_template
import os
import base64
from PIL import Image
import requests
from io import BytesIO
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Loading Gemini API key from .env file
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route to render the HTML page
@app.route('/')
def index():
    return render_template('Template.html')

# Route to handle image upload
@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        # Get JSON payload
        data = request.get_json()
        base64_image = data.get('image')

        if not base64_image:
            return jsonify({"error": "No image provided"}), 400

        # Decode the Base64 image string
        image_data = base64.b64decode(base64_image)
        image = Image.open(BytesIO(image_data))

        # Process the image (or call your model for description)
        description = get_image_description(image)  # Replace with your model logic

        return jsonify({"description": description})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Function to communicate with Gemini API for image description
def get_image_description(image):
    model=genai.GenerativeModel("gemini-1.5-flash")
    prompt="""
    Analyze the uploaded image and generate a concise description of its content. Focus on identifying key elements such as objects, people, activities, emotions, or scenes depicted in the image. Ensure the description is clear, human-readable, and limited to 2-3 sentences.
    """
    response=model.generate_content([prompt,image])
    if response.text:
        return response.text
    else:
        return "Error: Could not generate description"

if __name__ == "__main__":
    app.run(debug=True)
