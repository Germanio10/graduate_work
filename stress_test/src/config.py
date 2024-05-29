import logging


class Config:
    conf_name = 'stress_test'
    pacing_sec = 0.1
    api_host = 'http://127.0.0.1:84'


class LogConfig:
    logger = logging.getLogger('stress_test')
    logger.setLevel('DEBUG')
    file = logging.FileHandler(filename='test_logs.log')
    file.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
    logger.addHandler(file)
    logger.propagate = False


logger = LogConfig().logger
cfg = Config()
