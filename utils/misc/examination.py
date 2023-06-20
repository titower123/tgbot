import logging

from core.config import admins, operators, moderators


def examination():
    logging.info(f'Администраторы: {str.join(",", admins)}') if len(admins) != 0 else logging.info('Администраторы не добавлены')
    logging.info(f'Операторы: {str.join(",", operators)}') if len(operators) != 0 else logging.info('Операторы не добавлены')
    logging.info(f'Модераторы: {str.join(",", moderators)}') if len(moderators) != 0 else logging.info('Модераторы не добавлены')

