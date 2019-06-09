from flask import Flask, render_template, request
from feature import (
    ImageDescriptor,
    Searcher,
    Database,
    loadmodel,
    BASE_DIR
)
# from source import feature
# from source.feature import *
from werkzeug.utils import secure_filename
import os

app = Flask(__name__,
    template_folder= os.path.join(BASE_DIR, "templates")
)

IMG_PATH = "/static/images/"
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static/images')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


if __name__ == '__main__':
    cluster = loadmodel()
    searcher = Searcher(cluster)

    app.static_folder=BASE_DIR + app.static_url_path
    @app.route("/", methods=["GET", "POST"])
    def index():
        return render_template('index.html')
        
    @app.route("/results", methods=["GET", "POST"])
    def results():
        img_path = None
        img_src = None
        if request.method == "POST":
            if 'img-file' in request.files:
                file = request.files['img-file']
                img_src = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
                file.save(img_src)
                img = ImageDescriptor(img_src, True)
                img_src = os.path.join(IMG_PATH, file.filename)
            else:
                img_path = request.form['img-url']
                # img = ImageDescriptor(url)
                img_src = img_path

        
        res = searcher.search(img_path, 20)
        if not res:
            return render_template('notfound.html')

        images = []
        for img in res:
            images.append({
                "path": img[1][1],
                "accuracy": img[1][0].tolist()[0][0]
            })
        return render_template(
            "results.html",
            images=images,
            img_src=img_src.replace(app.static_folder, "/static")
        )

    app.run(debug=True)