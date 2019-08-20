import logging

# set up logging to file - see previous section for more details
logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='watch_events.log',
                    filemode='w')
logger = logging.getLogger('etcd_client_logger')


def message(msg):
    logger.info(msg)
    print(msg)


def critical_message(msg):
    logger.critical(msg)
    print(msg)


def warning_message(msg):
    logger.warning(msg)
    print(msg)
