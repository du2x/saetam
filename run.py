from flask import send_from_directory

from application import app

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/static/<path:path>')
def send_css(path):
    return send_from_directory('css', path)


app.run(debug=True)
