from dotenv import load_dotenv, dotenv_values, set_key


def get_config():
    """
    Get environment config
    :param key: The key of the config
    :return: The value of the config
    """
    config = dotenv_values('.env')
    return config

