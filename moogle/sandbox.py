# Google related imports
import httplib2
from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials

# Start the mocks
import moogle
mock = moogle.mock_gcs()
mock.start()


email = "moogle@google.com"
scope = "https://www.googleapis.com/auth/devstorage.full_control"
f = file("/home/jeff/Git/gcs_dev/key.p12", "rb")
key = f.read()
f.close()

credentials = SignedJwtAssertionCredentials(email, key, scope=scope)
service = build("storage", "v1beta2", http=credentials.authorize(httplib2.Http()))

res1 = service.buckets().insert(project="mock_project", body={"name": "test"})
foo = res1.execute()

#=====
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