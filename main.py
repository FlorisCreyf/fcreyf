from functools import wraps
from flask import Flask, abort, request, render_template, redirect, make_response

app = Flask(__name__)

def verify_domain(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Setting the canonical in the HTTP header is another option.
        if request.host.endswith("appspot.com"):
            return redirect("https://www.fcreyf.com" + request.path, 301)
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
@verify_domain
def create_index_page():
    return render_template("index.html")

@app.route("/article/<title>")
@verify_domain
def create_article_page(title):
    filename = title + ".html"
    try:
        return render_template(filename, name=title.replace("-", " "))
    except:
        return abort(404)

@app.route("/about")
@verify_domain
def create_about_page():
    return render_template("about.html")

@app.errorhandler(404)
def create_404_page(error):
    return render_template("error.html", error=error), 404

@app.errorhandler(500)
def create_500_page(error):
    return render_template("error.html", error=error), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
