from flask import Flask, render_template, request, redirect, url_for, send_file
import os
import main
import base64
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    if 'image' not in request.files:
        return redirect(url_for('index'))

    image = request.files['image']
    if image.filename == '':
        return redirect(url_for('index'))

    # Save the uploaded image to a specific folder
    upload_folder = 'uploads'
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    image_path = os.path.join(upload_folder, image.filename)
    image_path = 'image.jpg'  # Use a fixed path for the uploaded image
    image.save(image_path)

    # Process the image and generate the song text
    captured_text = main.image2lyrics(image_path)  # Adjust this line to use your image processing function

    main.text2audio(captured_text)
    with open('hello.mp3', 'rb') as audio_file:
        audio_data = base64.b64encode(audio_file.read()).decode('utf-8')

    # Pass the path of the uploaded image to the result template
    uploaded_image_path = image_path  # Replace this with the actual path to the uploaded image

    return render_template('result.html', song_text=captured_text, audio_data=audio_data, uploaded_image_path=uploaded_image_path)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)