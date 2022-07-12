import json
import socket
from flask import make_response
from hetch_utilities.models.http_codes import http_codes

class ResponseModel():
    def __init__(self, cd: int, rs=None, d=None, msg=None):
        try:
            # parse the code to a proper type
            self.status_code = str(cd)

            if msg != None:
                self.status_message = msg
            else:
                # propely format the response message
                self.status_message = ' '.join(
                    http_codes[cd][0].capitalize().split('_'))

            if rs != None:
                self.reason = rs

            if d != None:
                self.data = d

            # Incase one of the Pods is faulty in production
            self.pod = socket.gethostname()

        except KeyError as error:
            print('Invalid status code')

    def to_json(self):
        response = make_response(json.dumps(
            self.__dict__), int(self.status_code))
        response.headers['Content-Type'] = 'application/json'
        return response
