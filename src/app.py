import logging
import logging.handlers


log_handler = logging.handlers.SysLogHandler()
log_handler.ident = 'ip2w'
logging.basicConfig(level=logging.INFO, handlers=[log_handler])


def application(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    logging.info('new request')
    return [b"Hello World"]
