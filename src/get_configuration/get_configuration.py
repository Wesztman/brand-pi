import configparser


class GetConfiguration(object):
    def __init__(self, cfg_path):
        self.cfg = configparser.ConfigParser()
        self.cfg.read(cfg_path)

    def as_string(self, section, my_setting):
        try:
            ret = self.cfg.get(section, my_setting)
        except configparser.NoOptionError:
            ret = None
        return ret

    def as_int(self, section, my_setting):
        try:
            ret = self.cfg.getint(section, my_setting)
        except configparser.NoOptionError:
            ret = None
        return ret

    def as_float(self, section, my_setting):
        try:
            ret = self.cfg.getfloat(section, my_setting)
        except configparser.NoOptionError:
            ret = None
        return ret

    def as_bool(self, section, my_setting):
        try:
            ret = self.cfg.getboolean(section, my_setting)
        except configparser.NoOptionError:
            ret = None
        return ret