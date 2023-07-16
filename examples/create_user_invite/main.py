from orbitalcyber import OrbitalClient
from argparse import ArgumentParser
from os import environ
import logging
from sys import exit
import requests
from json import dumps, loads

parser = ArgumentParser(description='basic example of how to fetch a list of tasks from OrbitalCyber.')
parser.add_argument('--key', default=environ.get('ORBITAL_KEY'), help='the API client key.', required=True)
parser.add_argument('--secret', default=environ.get('ORBITAL_SECRET'), help='the API client secret.', required=True)
parser.add_argument('--id', default=environ.get('ORBITAL_ID'), help='the API client id (guid).')
parser.add_argument('--disable-ssl-verification', action='store_true', help='disable SSL verification', default=False)
parser.add_argument('--add-http-proxy', action='append', default=[], help='add http proxy for connections')
parser.add_argument('--add-https-proxy', action='append', default={}, help='add https proxy for connections')
parser.add_argument('--api-host', default='https://app.orbitalcyber.com', help='the orbitalcyber instance you would like to communicate with')
parser.add_argument('-d', '--debug', action='store_true', default=False, help='enable debug logging')
parser.add_argument('--invite-email', required=True, help='the email of the user you would like to invite')
parser.add_argument('--superUser', action='store_true', default=False, help='whether the new user should be a super user in OrbitalCyber.')
args = parser.parse_args()
level = logging.INFO
if args.debug:
    level = logging.DEBUG
logging.basicConfig(format="%(asctime)s [%(levelname)s]: %(message)s", level=level)
proxy_config = {'http': args.add_http_proxy, 'https': args.add_https_proxy}
client = OrbitalClient(args.id, args.key, args.secret, disable_ssl_verification=args.disable_ssl_verification,
                       proxy_config=proxy_config, api_host=args.api_host)
logging.info(f"Authenticated to the OrbitalAPI at instance {args.api_host} successfully.")
resp = client.post('/api/auth/company-mgmt/invite', json={'email': args.invite_email, 'superUser': args.superUser})
if resp.status_code == 200:
    print(f"Successfully created user invite")
print(resp.content)
if resp.status_code == 200:
    resp = client.delete(f'/api/auth/company-mgmt/invite/{resp.json()["invite"].get("id")}')
    if resp.status_code == 200:
        print(f"Successfully deleted invite")
    print(resp.content)