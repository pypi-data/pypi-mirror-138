import json
import pathlib

from dateutil import tz, parser


class TimeAttribute(str):
    def local(self):
        return parser.isoparse(self).astimezone(tz.tzlocal()).isoformat()

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self)


class TokenFileStorage(object):
    def __init__(self, token_filepath):
        if not isinstance(token_filepath, pathlib.Path):
            self.token_filepath = pathlib.Path(token_filepath)

    def read_token(self):
        if not self.token_filepath.is_file():
            return None
        else:
            with open(self.token_filepath, 'r') as f:
                return json.load(f)

    def write_token(self, token):
        with open(self.token_filepath, 'w') as f:
            json.dump(token, f, indent=4)

    @property
    def token(self):
        return self.read_token()

    @token.setter
    def token(self, token):
        self.write_token(token)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()
