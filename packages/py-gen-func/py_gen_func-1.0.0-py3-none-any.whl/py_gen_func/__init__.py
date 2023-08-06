import logging

logger = logging.getLogger("py_gen_func")
console_handler = logging.StreamHandler()

logger.setLevel(logging.INFO)
logger.addHandler(console_handler)
