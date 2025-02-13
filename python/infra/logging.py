import logging
import os


mainLogger = None
loggerInitialized : bool = False

def getMainLogger():
    if not loggerInitialized:
        mainLogger = logging.getLogger(__name__)
        logging.basicConfig(
            filename='docsFlow.log',
            level=logging.INFO,  # Set the logging level to INFO
            format='%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s() - %(message)s'  # Define log message format
        )

        mainLogger.info('Logging initialized')
        mainLogger.info("{}".format(os.environ['PYTHONPATH']))
    
    return mainLogger
    