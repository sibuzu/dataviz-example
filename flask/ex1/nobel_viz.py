import flask
app = flask.Flask(__name__)

nobel_winners = [
    {'catagory': 'Physics',
     'name': 'Albert Einstein',
     'nationality': 'Swiss',
     'sex': 'male',
     'year': 1921},
    {'catagory': 'Physics',
     'name': 'Paul Dirac',
     'nationality': 'British',
     'sex': 'male',
     'year': 1933},
    {'catagory': 'Chemistry',
     'name': 'Marie Curie',
     'nationality': 'Polish',
     'sex': 'female',
     'year': 1911},
]

@app.route("/")
def hello():
    return "Hello World"

@app.route("/demolist")
def demo_list():
    return flask.render_template('testj2.html',
                heading="A titile winners' list",
                winners=nobel_winners)

if __name__ == "__main__":
    app.run(port=8000, debug=True)
