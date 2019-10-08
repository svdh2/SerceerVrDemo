from flask import Flask, send_from_directory
import os
import socket
import netifaces as ni
import click


STATIC_FILES_DIR = 'static'

def get_ip(nic=None):
    if nic is None:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP
    else:
        ip = ni.ifaddresses(nic)[ni.AF_INET][0]['addr']
        return ip


static_files_dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), STATIC_FILES_DIR)
print(f'static_path:{static_files_dir_path}')
app = Flask(__name__, static_folder=STATIC_FILES_DIR)

app = Flask(__name__)


@app.route('/', methods=['GET'])
def serve_index():
    return send_from_directory(static_files_dir_path, 'app_index.html')

@click.group()
def cli():
    pass

@click.command()
@click.option('--nic', default=None, help='Network interface to bind to.')
def serve(nic):
    ip = get_ip(nic)
    print(f'binding to network {nic} with ip:{ip}')
    app.run(host=ip, port=8081, debug=True)

@click.command()
def ls_nic():
    for item in ni.interfaces():
        print(f'interface: {item}')

cli.add_command(serve)
cli.add_command(ls_nic)

if __name__ == '__main__':
    cli()