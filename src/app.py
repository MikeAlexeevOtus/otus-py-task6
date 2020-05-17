import logging
import logging.handlers
import json
import os

import requests

DEFAULT_CONFIG_PATH = '/usr/local/etc/ip2w/config.json'

log_handler = logging.handlers.SysLogHandler(address='/dev/log')
log_handler.ident = 'ip2w'
logging.basicConfig(level=logging.INFO, handlers=[log_handler])


config_path = os.getenv('CONFIG', DEFAULT_CONFIG_PATH)
if not os.path.exists(config_path):
    raise RuntimeError('config file doesn\'t exist')
with open(config_path) as f:
    CONFIG = json.load(f)

if CONFIG.get('debug'):
    log_handler.setLevel(logging.DEBUG)
    logging.getLogger().setLevel(logging.DEBUG)


def get_city(ipinfo_url, addr, proxies=None):
    resp = requests.get(f'{ipinfo_url}/{addr}', proxies=proxies)
    resp.raise_for_status()
    return resp.json()['city']


def get_weather(weather_api_url, token, city, proxies=None):
    params = {
        'access_key': token,
        'query': city
    }
    resp = requests.get(weather_api_url, params=params, proxies=proxies)
    resp.raise_for_status()
    return resp.json()


def application(env, start_response):
    start_response('200 OK', [('Content-Type', 'application/json')])
    ipaddr = env['PATH_INFO'].strip('/')
    logging.debug('config: %s', CONFIG)

    ipinfo_api_url = CONFIG['ipinfo_api_url']
    weather_api_url = CONFIG['weather_api_url']
    weather_api_token = CONFIG['weather_api_token']
    proxies = CONFIG.get('proxies')

    # TODO - addr validation
    logging.debug('new request with ip: %s', ipaddr)
    try:
        city = get_city(ipinfo_api_url, ipaddr)
    except Exception:
        logging.exception('failed to get city, args: %s', (ipinfo_api_url, ipaddr, proxies))
        raise

    logging.debug('resolved city: %s', city)
    try:
        weather_info = get_weather(weather_api_url, weather_api_token, city, proxies)
    except Exception:
        logging.exception('failed to get weather, args: %s', (weather_api_url, city, proxies))
        raise

    return [json.dumps(weather_info).encode('utf-8')]
