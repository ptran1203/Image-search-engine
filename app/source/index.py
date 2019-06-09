from flask import Flask, render_template, request, make_response
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
import json

app = Flask(__name__,
    template_folder= os.path.join(BASE_DIR, "templates")
)

IMG_PATH = "/static/images/"
# UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)).replace(), '/static/images')
UPLOAD_FOLDER = BASE_DIR + "/static/images"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


if __name__ == '__main__':
    cluster = loadmodel()
    searcher = Searcher(cluster)

    app.static_folder=BASE_DIR + app.static_url_path
    @app.route("/", methods=["GET", "POST"])
    def index():
        return render_template('index.html')
        
    @app.route("/test", methods=["GET", "POST"])
    def test():
        if (request.method == "POST"):
            # print('a')
            x = request.form['data']
            print(x)
        return render_template('index.html')




    @app.route("/results", methods=["GET", "POST"])
    def results():
        img_path = None
        img_src = None
        if request.method == "POST":
            from_url = None
            if 'fromUrl' in request.form.keys():
                from_url = request.form['fromUrl']
            print('XXXXX')
            print(from_url)
            if from_url is not None:
                print('url')
                img_path = request.form['imageUrl']
                img_src = img_path
            else:
                print('file')
                file = request.files['file']
                img_src = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
                print(type(img_src))
                file.save(img_src)
                img = ImageDescriptor(img_src)
                img_src = os.path.join(IMG_PATH, file.filename)
                img_path = BASE_DIR+"/"+img_src

        res = searcher.search(img_path, 20)
        if not res:
            return render_template('notfound.html')

        images = []
        for img in res:
            images.append({
                "path": img[1][1],
                "accuracy": img[1][0].tolist()[0][0]
            })
        resp = make_response(json.dumps({'data': images}))
        resp.status_code = 200
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

    app.run(debug=True)