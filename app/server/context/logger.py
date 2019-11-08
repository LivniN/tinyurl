import logging
from app.server.context import config

log_format = '%(asctime)s %(name)s %(levelname)s %(message)s'
fmt = logging.Formatter(log_format)
level = config['logger']['level']
logging.basicConfig(format=log_format, level=level, filename=config['logger']['path'])
log = logging.getLogger('server')
console_handler = logging.StreamHandler()
console_handler.setLevel(level)
console_handler.setFormatter(fmt)
log.addHandler(console_handler)
