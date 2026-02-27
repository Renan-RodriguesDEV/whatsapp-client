import datetime
import logging
import os
import sys


def setup_logger(name: str = "whatsapp_client", save_to_file: bool = False):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    logger.propagate = False
    if logger.handlers:
        return logger

    # criando um formatter padrão para o logger
    formatter = logging.Formatter(
        "%(asctime)s | %(filename)s:%(lineno)d | %(levelname)s | %(message)s",
        "%Y-%m-%d %H:%M:",
    )
    # criando um handler para o console
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)

    # criando um handler para arquivos
    if save_to_file:
        if not os.path.exists("logs"):
            os.makedirs("logs")
        current_date = datetime.datetime.now().strftime("%Y%m%d")
        fh = logging.FileHandler(f"logs/{name}_{current_date}.log")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)

    # adicionando os handlers ao logger
    logger.addHandler(ch)
    if save_to_file:
        logger.addHandler(fh)

    return logger


logger = setup_logger()
