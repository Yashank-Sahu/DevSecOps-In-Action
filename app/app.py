from flask import Flask, render_template, request
from rembg import remove
from PIL import Image
from io import BytesIO
import base64


class BackgroundRemover:
    def __init__(self):
        self.image_data = None

    def process_image(self, file):
        try:
            img = Image.open(file.stream)
            result = remove(img)

            img_io = BytesIO()
            result.save(img_io, "PNG")
            img_io.seek(0)

            self.image_data = base64.b64encode(img_io.getvalue()).decode('utf-8')
        except Exception as e:
            print(f"An error occurred: {e}")
            self.image_data = None

    def get_image_data(self):
        return self.image_data


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    remover = BackgroundRemover()
    if request.method == "POST":
        file = request.files["image"]
        remover.process_image(file)

    return render_template("index.html", image_data=remover.get_image_data())
