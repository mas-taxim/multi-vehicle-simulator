import os
import sys
import getopt


def resolve_path(path: str) -> str:
    is_relative = not path.startswith('/')
    abspath = os.path.abspath
    if is_relative:
        base = os.path.abspath(os.getcwd())
        return abspath(os.path.join(base, path))
    return abspath(path)


class Options(dict):
    def __init__(self, *args, **kwargs):
        help_text = "\n".join([
            "  -h, --help: Display this help text",
            "  -l, --log-file: Log file path to display animation",
        ])
        self.__dict__ = dict(
            help=help_text,
            logfile="",
        )
        self.update(dict(*args, **kwargs))  # use the free update to set keys

    def __getitem__(self, key: str) -> str:
        return self.__dict__[self._keytransform(key)]

    def __setitem__(self, key: str, value: str) -> None:
        self.__dict__[self._keytransform(key)] = value

    def _keytransform(self, key: str) -> str:
        return key.lower().replace("-", "").replace("_", "")

    def __repr__(self) -> str:
        return self.__dict__.__repr__()


def get_options(exit_on_error: bool = True) -> Options:
    arguments = sys.argv

    FILE_NAME = arguments[0]

    parsed = Options()

    try:
        # `h`: short option
        # `l:`: short option with value
        options, other_arguments = getopt.getopt(arguments[1:],
                                                 "hl:", ["help", "log-file="])

    except getopt.GetoptError:
        if exit_on_error:
            print(FILE_NAME, '\n', parsed["help"])
            sys.exit(2)
        return parsed

    for option, arg in options:
        if option in ("-l", "--log-file"):
            parsed["log-file"] = resolve_path(arg)

    return parsed
