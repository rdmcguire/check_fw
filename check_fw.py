#!/usr/bin/python3
##############################
# Author: Ryan McGuire
# Description: Server/Client firewall checker
# Version: 20211014.01
##############################
import argparse
import yaml
from lib.termcolor import colored
import socket

class firewall_tool:
    def __init__(self, config_file, verbose = False):
        self.config = dict()
        self.verbose = verbose
        self.listeners = list()
        self.load_config(config_file)

    def load_config(self, config_file):
        with open(config_file, 'r') as config_file:
            self.config = yaml.load(config_file, Loader=yaml.FullLoader)

    def run_checks(self):
        if 'client' in self.config.keys() and 'targets' in self.config['client'].keys():
            self.print_log('Running port checks',indent=0,bold=True)
            if len(self.config['client']['targets']) > 0:
                for target in self.config['client']['targets']:
                    self.print_log(f'Scanning host {target}',bold=True)
                    for port in self.config['client']['targets'][target]['ports']:
                        self.print_log(f'Testing port {target}:{port}...\t',newline=False,indent=2)
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        result = sock.connect_ex(( target, port ))
                        if result:
                            self.print_log('[CLOSED]', no_pre=True, sev='err')
                        else:
                            self.print_log('[OPENED]', no_pre=True, sev='good')

            else:
                self.print_log('Client defined with no targets, nothing to do, just gonna die',sev='err',bold=True)
        else:
            self.print_log('No client declared, nothing to do, just gonna die',sev='err',indent=0,bold=True)

    def prepare_server(self):
        if 'server' in self.config.keys():
            self.print_log('Found server declaration, running ports...',indent=0,bold=True)
            if 'ports' in self.config['server'].keys() and len(self.config['server']['ports']) > 0:
                self.print_log('Port declarations found, ensuring listeners on ports:')
                for port in self.config['server']['ports']:
                    self.print_log(str(port),indent=2)
                    self.server_port(port)
                return True
            else:
                self.print_log('No ports declared for server, abandoning server mode',sev='warn')
                return False
        else:
            self.print_log('No servers declared, skipping server mode',indent=0,bold=True,sev='warn')
            return False

    def server_port(self, port):
        if len(str(port).split(':')) == 2:
            addr = ( str(port).split(':')[0], int(str(port).split(':')[1]) )
        else:
            addr = ( '0.0.0.0', int(port) )
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if not sock.connect_ex(addr):
            self.print_log(f'Port {str(addr)} is listening',sev='good',indent=3)
        else:
            self.print_log(f'Port {str(addr)} not ready, starting...',indent=3)
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind(addr)
            server_socket.listen(10)
            self.listeners.append(server_socket)

    def start_server(self):
        if self.prepare_server():
            self.print_log('Ready to work, run the client...',indent=0,bold=True,sev='good')
            while True:
                for ss in self.listeners:
                    cs, addr = ss.accept()
                    data = cs.recv(1024)
                    self.print_log(f'Received ping from {addr}, sending pong...',indent=0,sev='good')
                    cs.send(str.encode('PONG'))
                    cs.close()
        else:
            self.print_log('No server stuff to do, just gonna die now')

    def print_log(self,msg,indent=1,sev='info',bold=False,no_pre=False,dt=False,newline=True):
		# Log Prefix
        if not no_pre:
            if sev == 'info':
                pre = colored('** ','cyan',attrs=['bold'])
            elif sev == 'good':
                pre = colored('** ','green',attrs=['bold'])
            elif sev == 'warn':
                pre = colored('*! ','yellow',attrs=['bold'])
            elif sev == 'err':
                pre = colored('!! !! ','red',attrs=['bold'])
            else:
                pre = colored('** ','cyan',attrs=['bold'])
        else:
            pre = ''
		# Timestamp
        if dt:
            pre = f'{colored(datetime.now(),"white","on_grey",attrs=["bold"])} {pre}'
		# Msg Style
        style = []
        if bold:
            style = ['bold']
        if no_pre:
            if sev == 'info':
                msg = colored(msg,'cyan',attrs=['bold'])
            elif sev == 'good':
                msg = colored(msg,'green',attrs=['bold'])
            elif sev == 'warn':
                msg = colored(msg,'yellow',attrs=['bold'])
            elif sev == 'err':
                msg = colored(msg,'red',attrs=['bold'])
            else:
                msg = colored(msg,'cyan',attrs=['bold'])
        msg = '\t'*indent + pre + colored(msg,attrs=style)
        if self.verbose:
            if newline:
                print(f'{msg}',flush=True)
            else:
                print(f'{msg}',end='',flush=True)

def main():
    parser = argparse.ArgumentParser(description='Client/Server Firewall Test Tool')
    parser.add_argument('-f', '--config', help='Config file location', required=True)
    parser.add_argument('-v', '--verbose', action='store_true', help='Be Verbose')
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('-c', '--client', action='store_true', help='Client Mode')
    mode.add_argument('-s', '--server', action='store_true', help='Server Mode')
    args = parser.parse_args()
    # Start up
    fwc = firewall_tool(args.config, args.verbose)

    if args.server:
        fwc.start_server()
    elif args.client:
        fwc.run_checks()
    else:
        print('No work to do, just gonna die now')

if __name__ == '__main__':
    main()
