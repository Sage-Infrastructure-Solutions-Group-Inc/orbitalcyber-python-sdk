from orbitalcyber import OrbitalClient
from argparse import ArgumentParser
from os import environ
import logging


parser = ArgumentParser(description='basic example of how to create a task with the OrbitalCyber API.')
parser.add_argument('--key', default=environ.get('ORBITAL_KEY'), help='the API client key.', required=True)
parser.add_argument('--secret', default=environ.get('ORBITAL_SECRET'), help='the API client secret.', required=True)
parser.add_argument('--id', default=environ.get('ORBITAL_ID'), help='the API client id (guid).')
parser.add_argument('--disable-ssl-verification', action='store_true', help='disable SSL verification', default=False)
parser.add_argument('--add-http-proxy', action='append', default=[], help='add http proxy for connections')
parser.add_argument('--add-https-proxy', action='append', default={}, help='add https proxy for connections')
parser.add_argument('--scanner', help='the GUID of the scanner', required=True)
parser.add_argument('--target', help='the scan task target', required=True)
parser.add_argument('--ports', help='the scan task target ports', required=True)
parser.add_argument('--api-host', default='https://app.orbitalcyber.com', help='the orbitalcyber instance you would like to communicate with')
parser.add_argument('-d', '--debug', action='store_true', default=False, help='enable debug logging')
args = parser.parse_args()
level = logging.INFO
if args.debug:
    level = logging.DEBUG
logging.basicConfig(format="%(asctime)s [%(levelname)s]: %(message)s", level=level)
proxy_config = {'http': args.add_http_proxy, 'https': args.add_https_proxy}
client = OrbitalClient(args.id, args.key, args.secret, disable_ssl_verification=args.disable_ssl_verification,
                       proxy_config=proxy_config, api_host=args.api_host)
logging.info(f"Authenticated to the OrbitalAPI at instance {args.api_host} successfully.")
SOFTWARE = 0 # OpenVAS
SOFTWARE_OPTIONS = {
    "alive_test": "tcp_syn",
    "alive_test_ports": "1-1000",
    "cvss_filter": 2,
    "expand_vhosts": True,
    "hosts_deny": "",
    "max_checks": 15,
    "max_hosts": 5,
    "optimize_test": True,
    "qod": 70,
    "safe_checks": True,
    "test_alive_hosts_only": True
}
resp = client.post('/api/scan/dropship/tasks', json={
    'target': args.target,
    'ports': args.ports,
    'software': SOFTWARE,
    'software_options': SOFTWARE_OPTIONS,
    'scanner_id': args.scanner
})
if resp.status_code == 200:
    print(f'Got response from server: \n{resp.content}')
else:
    print(f"Got status code: {resp.status_code}\n{resp.content}")