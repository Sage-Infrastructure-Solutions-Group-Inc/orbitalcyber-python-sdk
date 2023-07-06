from orbitalcyber import OrbitalClient
from argparse import ArgumentParser
from os import environ
import logging
from sys import exit
import requests
from json import dumps, loads
from bz2 import decompress as bz_decompress
from zlib import decompress as zlib_decompress

parser = ArgumentParser(description='basic example of how to fetch a list of reports from OrbitalCyber.')
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
reports = client.get('/api/scan/dropship/reports')
if reports.status_code != 200: exit(1)
reports = reports.json()
print(dumps(reports, indent=2))
report_list = reports.get('page')
if len(report_list) > 0:
    report_download_link = client.get(f'/api/scan/dropship/report/download/{report_list[0].get("id")}')
    if report_download_link.status_code != 200: exit(1)
    report_download_url = report_download_link.json().get('url')
    data = requests.get(report_download_url).content
    # OrbitalCyber used to use bzip compression. Some users may need to include the following code for compatibility.
    try:
        data = zlib_decompress(data)
    except (ValueError, OSError, TypeError):
        data = bz_decompress(data)
    data = loads(data)
    print(dumps(data, indent=4))