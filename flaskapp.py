from flask import Flask, render_template, send_from_directory, request
from sequence_finder import finder

app = Flask(__name__)
app.config.from_pyfile('flaskapp.cfg')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<path:resource>')
def serveStaticResource(resource):
    return send_from_directory('static/', resource)


@app.route("/test")
def test():
    return render_template("sequence_finder/math.html")


@app.route("/finder", methods=[ 'GET'])
def sequence_finder():
    return render_template("sequence_finder/index.html")

@app.route("/finder_exec", methods=[ 'POST'])
def exec_finder():
    return finder.execute(request.form['values'])

if __name__ == '__main__':
    app.run()
