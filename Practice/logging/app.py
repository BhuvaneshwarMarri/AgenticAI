import logging

logging.basicConfig(
    # filename='app.log',
    # filemode='w',
    level = logging.DEBUG,
    format = '%(asctime)s-%(name)s-%(levelname)s-%(message)s',
    datefmt = '%Y-%m-%d %H:%M:%S',
    # force = True
    handlers = [
        logging.FileHandler("app1.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("ArithmeticApp")


def add(a, b):
    res = a+b
    logger.debug(f"Adding {a} + {b} = {res}")
    return res

def subtract(a, b):
    res = a-b
    logger.debug(f"Subtracting {a} - {b} = {res}")
    return res

def multiply(a, b):
    res = a*b
    logger.debug(f"Multiplying {a} * {b} = {res}")
    return res

def divide(a, b):
    if b == 0:
        logger.error("Division by zero attempted!")
        return None
    res = a//b
    logger.debug(f"Dividing {a} // {b} = {res}")
    return res

add(10, 15)
subtract(20, 5)
multiply(3, 7)
divide(16, 4)
divide(10, 0)