import logging

logging.basicConfig(filename='output.log')
logger = logging.getLogger(__name__)

logger.debug('here')
logger.warn('it is warn: ', 123)
