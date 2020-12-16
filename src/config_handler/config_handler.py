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


def config_file_listener(config_file):
    # Initialize inotify object
    inotify = INotify()
    watch_flags = flags.MODIFY
    wd = inotify.add_watch(config_file, watch_flags)

    while True:
        # Watch config file changes
        readable, _, _ = select.select([inotify], [], [])

        if inotify in readable:
            for event in inotify.read():
                for flag in flags.from_mask(event.mask):
                    logging.info("Config file changed")
                    # Do stuff