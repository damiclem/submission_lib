import logging
import secrets

logging.basicConfig(level=logging.DEBUG,
                    filename='logger.log',
                    filemode='w',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


def make_token():
    """
    Creates a cryptographically-secure, URL-safe string
    """
    return secrets.token_urlsafe(16)


def param_dict_to_str(param_dict):
    tmp = ""
    for p, pval in param_dict.items():
        tmp += " {} {}".format(pval["flag"].strip(), pval["value"].strip())
    return tmp.strip()
