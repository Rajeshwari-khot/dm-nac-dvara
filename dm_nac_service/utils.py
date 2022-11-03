from configparser import ConfigParser

env = ConfigParser()
env.read('dm_nac_service/resource/env.ini')

def _raise(msg): raise Exception(msg)


def get_env(section, option, default: str) -> str: return env[section][option] if env.has_option(section, option) else default

def get_env_or_fail(section, option, msg) -> str: return env[section][option] if env.has_option(section, option) else _raise(msg)
