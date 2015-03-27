# set up tor session with Python
# reference: https://stem.torproject.org
import socket
import urllib
import socks
import stem.process
from stem.util import term

SOCKS_PORT = 7000

# Set socks proxy and wrap the urllib module
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', SOCKS_PORT)
socket.socket = socks.socksocket

# Perform DNS resolution through the socket
def getaddrinfo(*args):
 return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]

socket.getaddrinfo = getaddrinfo

# Start an instance of Tor configured to only exit through Russia. This prints
# Tor's bootstrap information as it starts. Note that this likely will not
# work if you have another Tor instance running.

def print_bootstrap_lines(line):
  if "Bootstrapped " in line:
    print term.format(line, term.Color.BLUE)

print term.format("Starting Tor:\n", term.Attr.BOLD)

tor_process = stem.process.launch_tor_with_config(
  config = {
    'SocksPort': str(SOCKS_PORT),
    'ExitNodes': '{ru}',
  },
  init_msg_handler = print_bootstrap_lines,
)

print term.format("\nChecking our endpoint:\n", term.Attr.BOLD)

# Stop tor
#tor_process.kill()  
