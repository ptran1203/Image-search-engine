from flask import Flask, render_template, request
from searcher.searcher import (
    ImageDescriptor,
    Searcher,
    Database,
)
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)

IMG_PATH = "/static/images/"
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static/images')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route("/", methods=["GET", "POST"])
def index():
    return render_template('index.html')
    
@app.route("/results", methods=["GET", "POST"])
def results():
    img = None
    path = None
    if request.method == "POST":
        if 'img-file' in request.files:
            file = request.files['img-file']
            img = ImageDescriptor(file, False)
            path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
            file.save(path)
        else:
            url = request.form['img-url']
            img = ImageDescriptor(url, False)
            path = url
    
    db = Database(True)
    searcher = Searcher(img.color_feature(), db.data)
    res = searcher.search(10)
    for r in res:
        print(r)
    if not res:
        return "not found"

    images = []
    for r in res:
        path = IMG_PATH + r[0]
        accuracy = round(r[1], 2)
        images.append({
            "path": path,
            "accuracy": accuracy
        })

    return render_template(
        "results.html",
        images=images,
        img_src=(request.form['img-url'] or False)
    )

if __name__ == "__main__":
    app.run(debug=True)