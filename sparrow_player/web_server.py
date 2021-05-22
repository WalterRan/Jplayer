from threading import Thread
from flask import Flask

# @ -------- RESTAPI --------
app = Flask(__name__)


@app.route('/')
def hello_world():
    return "hello world"


@app.route('/title/', methods=['GET'])
def rest_get_title():
    return str(player.get_title())


# curl --request POST 127.0.0.1:5000/next/
@app.route('/next/', methods=['POST'])
def rest_post_next():
    return str(player.stop())


def web_server():
    app.run()



# 4. Start web interface
t2 = Thread(target=web_server)
t2.start()


