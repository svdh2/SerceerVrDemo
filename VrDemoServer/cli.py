import socket
import netifaces as ni
import click

from VrDemoServer import server

def get_ip(nic=None):
    """Returns the IP adress associated with a particular network adapter
    :param nic If None is provided, the ip adress returned is the one of the default adapter else it will \
               return the address of one of the adapter that can reach google's DNS at IP 8.8.8.8

    """
    if nic is None:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('8.8.8.8', 1))
            IP = s.getsockname()[0]
        except:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP
    else:
        ip = ni.ifaddresses(nic)[ni.AF_INET][0]['addr']
        return ip


@click.group()
def cli():
    pass


@click.command()
@click.option('--nic', default=None, help='Network interface to bind to, if not provided will connect to the first adapter thant can reach the internet.')
def serve(nic):
    """Starts the server."""
    ip = get_ip(nic)
    print(f'binding to network {nic} with ip:{ip}')
    server.run_server(ip=ip)

@click.command()
def ls_nic():
    """ Lists all the available network devices"""
    for item in ni.interfaces():
        print(f'interface: {item}')


cli.add_command(serve)
cli.add_command(ls_nic)

if __name__ == '__main__':
    cli()