from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
from io import BytesIO
from PIL import Image
import json
import os
import google.generativeai as genai

app = Flask(__name__)
CORS(app)
api_key = "AIzaSyDsz2p9WpV1vQ8wAql9mR2TDoysuJL4cmk"
# Load Gemini API key
try:
    genai.configure(api_key=api_key)
except KeyError:
    print("Error: GOOGLE_API_KEY environment variable not set.")
    genai_available = False
else:
    genai_available = True

@app.route('/generate', methods=['POST'])
def generate():
    # return jsonify({"gemini_response":"okay done!"})
    try:
        data = request.json
        image_data = data.get("image")
        prompt = "Extract the text from image"
        if not genai_available:
            return jsonify({"error": "Gemini API key not configured."}), 500

        if not image_data:
            return jsonify({"error": "No image provided."}), 400

        # Decode image
        _, base64_data = image_data.split(",", 1)
        image_bytes = base64.b64decode(base64_data)
        image_pil = Image.open(BytesIO(image_bytes))

        # Convert PIL Image to Gemini API image object
        # image_gemini = genai.Part.from_data(mime_type="image/png", data=image_bytes)

        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([prompt, image_pil])  # Send image and prompt
        gemini_response = response.text


        return jsonify({"gemini_response": gemini_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
