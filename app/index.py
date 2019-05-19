from flask import Flask, render_template, request
from searcher.searcher import (
    get_img_from_url,
    get_img,
    get_data,
    search,
    histogram
)

IMG_PATH = "/static/images/copydays_original/"

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template('index.html')
    
@app.route("/results", methods=["GET", "POST"])
def results():
    url = request.form['img-url'] or False
    # print(get_img_from_url(url))
    res = search(
        histogram(get_img_from_url(url) if "http" in url else get_img(url)),
        get_data()
    ) if url else False

    # print(res)
    images = []
    for name in res:
        path = IMG_PATH + name[0]
        images.append(path)

    return render_template(
        "results.html",
        images=images,
        img_src=(IMG_PATH + url if "http" not in url else url)
    )

if __name__ == "__main__":
    app.run()