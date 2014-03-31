__author__ = 'jeff'


import re

from jinja2 import Template

from .models import gcs_backend
from .errors import *

class Response(object):

    def __init__(self, backend):
        self.backend = backend

    def response(self, request, full_url, headers):
        if (request.path.find("/o?") > -1 or request.path.find("/o/") > -1):
            return ObjectResponse.object_response(request, full_url, headers)
        else:
            return BucketResponse.bucket_response(request, full_url, headers)



class ObjectResponse(object):
    def __init__(self, backend):
        self.backend = backend

    def object_response(self, request, full_url, headers):
        response = self._object_response(request, full_url)
        if isinstance(response, basestring):
            return 200, headers, response
        else:
            status_code, headers, response_content = response
            return status_code, headers, response_content

    def _object_response(self, request, full_url):
        if request.method == "POST":
            bucket_name = request.path[request.path.find("/b/")+3:request.path.find("/o?")]
            return self._post(request, bucket_name=bucket_name)
        if request.method == "GET":
            bucket_name = request.path[request.path.find("/b/")+3:request.path.find("/o/")]
            return self._get(request, bucket_name=bucket_name)

    def _post(self, request, bucket_name):
        key = self.backend.post_object(bucket_name, request.querystring["name"][0], request.body)
        response = Template(OBJECT_INSERT_RESPONSE)
        return json.dumps(response.render(key=key))

    def _get(self, request, bucket_name):
        object_name = request.path[request.path.find("/o/") + 3: request.path.find("?")]
        key = self.backend.get_object(bucket_name, object_name)
        if "json" in request.querystring["alt"]:
            response = Template(OBJECT_GET_RESPONSE)
            return json.dumps(response.render(key=key))
        else:
            return key.media


class BucketResponse(object):
    def __init__(self, backend):
        self.backend = backend

    def bucket_response(self, request, full_url, headers):
        response = self._bucket_response(request, full_url)
        if isinstance(response, basestring):
            return 200, headers, response
        else:
            status_code, headers, response_content = response
            return status_code, headers, response_content

    def _bucket_response(self, request, full_url):
        if request.method == "POST":
            return self._post(request, bucket_name = json.loads(request.body)["name"])

        elif request.method in ["PATCH", "PUT", "DELETE", "GET"]:
            raise Exception("%s is not implemented for %s" % (request.method, request.path))

        else:
            raise ValueError


    def _post(self, request, bucket_name):
        try:
            bucket = self.backend.post_bucket(bucket_name)
            visible = request.querystring.get("fields", None)
            if not visible:
                visible = bucket.visible_fields
            response = Template(BUCKET_INSERT_RESPONSE)
            return json.dumps(response.render(bucket=bucket, visible_fields=visible))
        except BucketAlreadyExists, error:
            return error.response

        response = Template(BUCKET_INSERT_RESPONSE)
        return json.dumps(response.render(bucket=bucket))

BaseResponse = Response(gcs_backend)
BucketResponse = BucketResponse(gcs_backend)
ObjectResponse = ObjectResponse(gcs_backend)

OBJECT_GET_RESPONSE = '''{
 "kind": "storage#object",
 "id": "{{ key.bucket }}/{{ key.name }}/{{ key.generation }}",
 "selfLink": "https://content.googleapis.com/storage/v1beta2/b/{{ key.bucket }}/o/{{ key.name }}",
 "name": "{{ key.name }}",
 "bucket": "{{ key.bucket }}",
 "generation": "{{ key.generation }}",
 "metageneration": "1",
 "contentType": "text/plain",
 "updated": "2014-03-31T20:33:28.289Z",
 "storageClass": "STANDARD",
 "size": " {{ key.size }}",
 "md5Hash": "VLDFjHzp8qi1UTURAu4JOA==",
 "mediaLink": "https://content.googleapis.com/storage/v1beta2/b/{{ key.bucket }}/o/{{ key.name }}?generation={{ key.generation }}&alt=media",
 "owner": {
    "entity": "{{ key.owner["entity"] }}",
    "entityId": "{{ key.owner["entityId"] }}"
  },
 "crc32c": "fPxmpw==",
 "etag": "COi9o7bPvb0CEAE="
}'''

OBJECT_INSERT_RESPONSE = '''{
 "bucket": "{{ key.bucket }}",
 "contentType": "text/plain",
 "crc32c": "fPxmpw==",
 "etag": "COi9o7bPvb0CEAE=",
 "generation": "1396298008289000",
 "id": "{{ key.id }}",
 "kind": "storage#object",
 "md5Hash": "VLDFjHzp8qi1UTURAu4JOA==",
 "mediaLink": "https://content.googleapis.com/storage/v1beta2/b/{{ key.bucket }}/o/{{ key.name }}",
 "metageneration": "1",
 "name": "{{ key.name }}",
 "owner": {
    "entity": "{{ key.owner["entity"] }}",
    "entityId": "{{ key.owner["entityId"] }}"
  },
 "selfLink": "https://content.googleapis.com/storage/v1beta2/b/{{ key.bucket }}/o/{{ key.name }}",
 "size": " {{ key.size }}",
 "storageClass": "STANDARD",
 "updated": "2014-03-31T20:33:28.289Z"
}'''


BUCKET_INSERT_RESPONSE = '''{
 "kind": "{{ bucket.kind }}",
 "id": "{{ bucket.id }}",
 "selfLink": "https://content.googleapis.com/storage/v1beta2/b/{{ bucket.id }}",
 "name": "{{ bucket.name }}",
 "timeCreated": "{{ bucket.timeCreated }}",
 "metageneration": "{{ bucket.metageneration }}",
 "owner": {
  "entity": "{{ bucket.owner["entity"] }}",
  "entityId": "{{ bucket.owner["entityId"] }}"
 },
 "location": "{{ bucket.location }}",
 "storageClass": "{{ bucket.storageClass }}",
 "etag": "{{ bucket.etag }}"
}'''


BUCKET_INSERT_RESPONSE = BUCKET_INSERT_RESPONSE.replace("\n", "").replace(" ", "")
OBJECT_INSERT_RESPONSE = OBJECT_INSERT_RESPONSE.replace("\n", "").replace(" ", "")
OBJECT_GET_RESPONSE    = OBJECT_GET_RESPONSE.replace("\n", "").replace(" ", "")