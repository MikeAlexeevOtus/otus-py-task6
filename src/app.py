import logging
import logging.handlers
import json
import os
from collections import namedtuple

import requests

DEFAULT_CONFIG_PATH = '/usr/local/etc/ip2w/config.json'
DEFAULT_API_REQUEST_TIMEOUT = 10    # seconds

log_handler = logging.handlers.SysLogHandler(address='/dev/log')
log_handler.ident = 'ip2w '
logging.basicConfig(level=logging.INFO, handlers=[log_handler])


ApiArgs = namedtuple('ApiArgs', 'url, token, params, timeout, proxies')


config_path = os.getenv('CONFIG', DEFAULT_CONFIG_PATH)
if not os.path.exists(config_path):
    raise RuntimeError('config file doesn\'t exist')
with open(config_path) as f:
    CONFIG = json.load(f)

if CONFIG.get('debug'):
    log_handler.setLevel(logging.DEBUG)
    logging.getLogger().setLevel(logging.DEBUG)


def get_city(api_args: ApiArgs) -> dict:
    url = '{base_url}/{ipaddr}'.format(base_url=api_args.url,
                                       ipaddr=api_args.params['ipaddr'])

    resp = requests.get(url, proxies=api_args.proxies, timeout=api_args.timeout)
    resp.raise_for_status()
    return resp.json()['city']


def get_weather(api_args: ApiArgs) -> dict:
    params = {
        'access_key': api_args.token,
        'query': api_args.params['city']
    }
    resp = requests.get(api_args.url, params=params,
                        proxies=api_args.proxies, timeout=api_args.timeout)
    resp.raise_for_status()
    return resp.json()


def application(env, start_response):
    start_response('200 OK', [('Content-Type', 'application/json')])
    ipaddr = env['PATH_INFO'].strip('/')
    # TODO - addr validation
    logging.debug('new request with ip: %s', ipaddr)

    logging.debug('config: %s', CONFIG)

    proxies = CONFIG.get('proxies')
    api_request_timeout = CONFIG.get('api_request_timeout', DEFAULT_API_REQUEST_TIMEOUT)

    city_api_args = ApiArgs(url=CONFIG['ipinfo_api_url'],
                            token=None,
                            params={'ipaddr': ipaddr},
                            timeout=api_request_timeout,
                            proxies=proxies)
    try:
        city = get_city(city_api_args)
    except Exception:
        logging.exception('failed to get city, args: %s', city_api_args)
        raise

    logging.debug('resolved city: %s', city)
    weather_api_args = ApiArgs(url=CONFIG['weather_api_args'],
                               token=CONFIG['weather_api_token'],
                               params={'city': city},
                               timeout=api_request_timeout,
                               proxies=proxies)

    try:
        weather_info = get_weather(weather_api_args)
    except Exception:
        logging.exception('failed to get weather, args: %s', weather_api_args)
        raise

    return [json.dumps(weather_info).encode('utf-8')]
