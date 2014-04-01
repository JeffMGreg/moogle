moogle
======

Mock + Google = moogle,  a mock of google cloud services.  More specifically it's a mock of google cloud storage and more specifically than that it just creates buckets and objects and gets objects without ever leaving the comfort of your localhost.  This project is based on https://github.com/spulec/moto

I hope to some day merge this with moto but until more functionality is added (and tests) it's going to sit here.

Here's an example:

```python
# Google related imports
import httplib2
from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials

# Start the mocks
import moogle
mock = moogle.mock_gcs()
mock.start()


email = "moogle@moogle.com"
scope = "https://www.googleapis.com/auth/devstorage.full_control"


f = file("/path/to/real/key.p12", "rb")
key = f.read()
f.close()

credentials = SignedJwtAssertionCredentials(email, key, scope=scope)
service = build("storage", "v1beta2", http=credentials.authorize(httplib2.Http()))

res1 = service.buckets().insert(project="mock_project", body={"name": "test"})
foo = res1.execute()

import io
from apiclient import http

key = http.MediaIoBaseUpload(io.BytesIO("this is a test"), 'text/plain')
bucket = "test"

res2 = service.objects().insert(bucket=bucket, name="test_key_name", media_body=key)
res2.execute()

res3 = service.objects().get(bucket=bucket, object="test_key_name")
res3.execute()

res4 = service.objects().get(bucket="foobar", object="test_key_name")
try:
    res4.execute()
except:
    pass

res5 = service.objects().get(bucket=bucket, object="foobar")
try:
    res5.execute()
except:
    pass

for x in xrange(10):
    service.objects().insert(bucket=bucket, name=str(x), media_body=key).execute()
```