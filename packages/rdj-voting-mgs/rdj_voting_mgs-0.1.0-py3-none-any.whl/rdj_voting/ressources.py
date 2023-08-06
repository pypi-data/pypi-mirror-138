import logging


def get_logger(name):
    _logger = logging.getLogger(name)
    _logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s : %(name)s : %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    _logger.addHandler(ch)
    return _logger


RDJ_VOTING = "https://rdj.mg/wp-content/plugins/rdjvoting/voter.php?list={}&hira={}"
RDJ_URL = "https://rdj.mg/"
