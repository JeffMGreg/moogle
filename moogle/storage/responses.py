__author__ = 'jeff'

import json
from jinja2 import Template

from .models import gcs_backend


def parse_key_name(pth):
    return pth.lstrip("/")


class ResponseObject(object):
    def __init__(self, backend, bucket_name_from_url, parse_key_name):
        self.backend = backend
        self.bucket_name_from_url = bucket_name_from_url
        self.parse_key_name = parse_key_name

    def bucket_response(self, request, full_url, headers):
        response = self._bucket_response(request, full_url, headers)
        if isinstance(response, basestring):
            return 200, headers, response
        else:
            status_code, headers, response_content = response
            return status_code, headers, response_content

    def _bucket_response(self, request, full_url, headers):

        import ipdb; ipdb.set_trace()

        bucket_name = json.loads(request.body).get("name", "failed_to_get_name")
        bucket = self.backend.post_bucket(bucket_name)

        foo = BUCKET_LIST_RESPONSE.replace("\n", "").replace(" ", "")
        response = Template(foo)
        return json.dumps(response.render(bucket=bucket))


GCSResponseInstance = ResponseObject(gcs_backend, "bucket_name_from_url", parse_key_name)

BUCKET_LIST_RESPONSE = """{'kind': 'storage#buckets',
                                'items': [
                                {
                                    'kind': '{{ bucket.kind }}',
                                    'id': '{{ bucket.id }}',
                                    'selfLink': 'https://content.googleapis.com/storage/v1beta2/b/{{ bucket.name }}',
                                    'name': '{{ bucket.name }}',
                                    'timeCreated': '{{ bucket.timeCreated }}',
                                    'metageneration': '{{ bucket.metageneration }}',
                                    'owner': {
                                        'entity': '{{ bucket.owner['entity'] }}',
                                        'entityId': '{{ bucket.owner['entityId'] }}'
                                    },
                                    'location': '{{ bucket.location }}',
                                    'storageClass': '{{ bucket.storageClass }}',
                                    'etag': '{{ bucket.etag }}'
                                },
                            ]
                        }"""

