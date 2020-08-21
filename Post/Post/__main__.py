from waitress import serve
from Post.app import app

app.run(host="127.0.0.1", port=5005, debug = True)