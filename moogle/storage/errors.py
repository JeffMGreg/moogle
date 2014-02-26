__author__ = 'jeff'

import json

class BucketAlreadyExists(Exception):

    @property
    def response(self):
        return json.dumps(dict(error={
            "errors": [
                {
                    "domain": "global",
                    "reason": "conflict",
                    "message": "You already own this bucket. Please select another name."
                }
            ],
            "code": 409,
            "message": "You already own this bucket. Please select another name."
        }))


class BucketNotEmpry(Exception):

    @property
    def response(self):
        return json.dumps(dict(error={
            "errors": [
                {
                    "domain": "global",
                    "reason": "conflict",
                    "message": "The bucket you tried to delete was not empty."
                }
            ],
            "code": 409,
            "message": "The bucket you tried to delete was not empty."
        }))

class BucketNotFound(Exception):

    @property
    def response(self):
        return json.dumps(dict(error={
            "errors": [
                {
                    "domain": "global",
                    "reason": "notFound",
                    "message": "Not Found"
                }
            ],
            "code": 404,
            "message": "Not Found"
        }))