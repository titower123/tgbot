import logging
import os
from core.config import LOGGING_PATH



logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,
                    filename=LOGGING_PATH,
                    # level=logging.DEBUG,  # Можно заменить на другой уровень логгирования.
                    )

logging.getLogger('aiogram.contrib').setLevel(logging.WARNING)

