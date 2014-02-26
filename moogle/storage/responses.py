__author__ = 'jeff'


import re

from jinja2 import Template

from .models import gcs_backend
from .errors import *

class ResponseObject(object):
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

        print request.method
        import ipdb; ipdb.set_trace()
        if request.method == "DELETE":
            bucket_name = full_url.split("/")[-1]
            self._delete(bucket_name)

        elif request.method == "GET":
            match = re.search("v1beta2/b/(?P<bucket_name>.+)", full_url.split("?")[0])
            bucket_name = None
            if match:
                bucket_name = match.groupdict()["bucket_name"]
            return self._get(request, bucket_name)

        elif request.method == "POST":
            return self._post(request, bucket_name = json.loads(request.body)["name"])

        elif request.method in ["PATCH", "PUT"]:
            raise NotImplemented

        else:
            raise ValueError

    def _delete(self, bucket_name):
        try:
            self.backend.delete_bucket(bucket_name)
            return json.dumps({})
        except BucketNotFound, error:
            return error.response
        except BucketNotEmpry, error:
            return error.response

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

    def _get(self, request, bucket_name):
        if not bucket_name:
            try:
                buckets = self.backend.list_buckets()
                response = Template(BUCKET_LIST_RESPONSE)

                visible = request.querystring.get("fields", None)
                if not visible:
                    visible = buckets[0].visible_fields

                response = Template(response)
                return json.dumps(response.render(buckets=buckets, visible_fields=visible))
            except:
                pass
        else:
            try:
                bucket = self.backend.get_bucket(bucket_name)
                response = Template(BUCKET_GET_RESPONSE)
                return json.dumps(response.render(bucket=bucket, visible_fields=bucket.visible_fields))
            except BucketNotFound, error:
                return error.response


GCSResponseInstance = ResponseObject(gcs_backend)

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


# ## ### Bucket GET Response -----
# 200 OK
#
# - Hide headers -
#
# cache-control:  private, max-age=0, must-revalidate, no-transform
# content-encoding:  gzip
# content-length:  289
# content-type:  application/json; charset=UTF-8
# date:  Wed, 26 Feb 2014 18:40:35 GMT
# etag:  CAE=
# expires:  Wed, 26 Feb 2014 18:40:35 GMT
# server:  GSE
BUCKET_GET_RESPONSE = '''{
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

# ## ### Bucket LIST Response -----
# 200 OK
#
# - Hide headers -
#
# cache-control:  private, max-age=0, must-revalidate, no-transform
# content-encoding:  gzip
# content-length:  390
# content-type:  application/json; charset=UTF-8
# date:  Wed, 26 Feb 2014 18:45:16 GMT
# expires:  Wed, 26 Feb 2014 18:45:16 GMT
# server:  GSE
BUCKET_LIST_RESPONSE = '''{
 "kind": "storage#buckets",
 "items": [

  {% for bucket in buckets %}
  {
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
  },
  {% endfor %}
 ]
}'''

# ## ### Bucket DELETE Response
# 204 No Content
#
# - Hide headers -
#
# cache-control:  no-cache, no-store, max-age=0, must-revalidate
# date:  Wed, 26 Feb 2014 19:55:37 GMT
# expires:  Fri, 01 Jan 1990 00:00:00 GMT
# pragma:  no-cache
# server:  GSE
BUCKET_DELETE_RESPONSE = '''{
}'''

BUCKET_GET_RESPONSE.replace("\n", "").replace(" ", "")
BUCKET_LIST_RESPONSE.replace("\n", "").replace(" ", "")
BUCKET_INSERT_RESPONSE.replace("\n", "").replace(" ", "")
BUCKET_DELETE_RESPONSE.replace("\n", "").replace(" ", "")