from flask import Flask, send_from_directory
import os
import connexion
from connexion.resolver import RestyResolver
from flask_socketio import SocketIO, send, emit

# Constants
STATIC_FILES_DIR = 'static'

# The application server
app = connexion.FlaskApp(__name__, specification_dir='swagger/', resolver=RestyResolver('VrDemoServer.api'))
flask_app = app.app
# We define the websocket feature
socketio = SocketIO(flask_app)

@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)
    emit('my response', "res"+message)

# We add the OpenApi definitions
app.add_api('demo2.yaml')

# we define that all static content will be served from the STATIC_FILES_DIR subdirectory
static_files_dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), STATIC_FILES_DIR)
app.static_folder = STATIC_FILES_DIR
app.add_url_rule(
                app.app.static_url_path + "/<path:filename>",
                endpoint="static",
                view_func=app.app.send_static_file,
            )

# we redirect the root index.thml to the app_index.html
@app.route('/', methods=['GET'])
def serve_index():
    return send_from_directory(static_files_dir_path, 'app_index.html')


# function to launch the server
def run_server(ip, port=8080, debug=False):
    # print('starting rest api')
    # app.run(host=ip, port=port, debug=debug)
    print('starting websocket')
    socketio.run(flask_app, host=ip, port=port, debug=debug)






