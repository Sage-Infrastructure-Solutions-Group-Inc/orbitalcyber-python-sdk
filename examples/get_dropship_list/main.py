from orbitalcyber import OrbitalClient
from argparse import ArgumentParser
from os import environ
import logging
from sys import exit
import requests
from json import dumps, loads

parser = ArgumentParser(description='basic example of how to fetch a list of lists from OrbitalCyber.')
parser.add_argument('--key', default=environ.get('ORBITAL_KEY'), help='the API client key.', required=True)
parser.add_argument('--secret', default=environ.get('ORBITAL_SECRET'), help='the API client secret.', required=True)
parser.add_argument('--id', default=environ.get('ORBITAL_ID'), help='the API client id (guid).')
parser.add_argument('--disable-ssl-verification', action='store_true', help='disable SSL verification', default=False)
parser.add_argument('--add-http-proxy', action='append', default=[], help='add http proxy for connections')
parser.add_argument('--add-https-proxy', action='append', default={}, help='add https proxy for connections')
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
dropship_lists_resp = client.get('/api/scan/dropship/lists')
last_scanner = None
if dropship_lists_resp.status_code == 200:
    lists = dropship_lists_resp.json()
    for list in lists.get('page'):
        print(f"Got list: {dumps(list, indent=4)}")
        last_list = list
try:
    if last_list:
        list_data_url = client.get(f'/api/scan/dropship/lists/{last_list.get("id")}')
        print(list_data_url)
        if list_data_url.status_code == 200:
            print(f"Got list download link: {dumps(list_data_url.json(), indent=4)}")
        list_data = requests.get(list_data_url.json().get('url'), proxies=proxy_config, verify=args.disable_ssl_verification)
        if list_data.status_code == 200:
            list_data = list_data.json()
            print(f"Got list data: {list_data}")
except NameError: pass
