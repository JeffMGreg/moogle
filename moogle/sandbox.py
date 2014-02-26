
# Google related imports
import httplib2
import pprint
from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials

# Start the mocks
import moogle
mock = moogle.mock_gcs()
mock.start()


email = "moogle@google.com"
scope = "https://www.googleapis.com/auth/devstorage.full_control"


f = file("/home/jeff/gcs-dev.p12", "rb")
key = f.read()
f.close()

credentials = SignedJwtAssertionCredentials(email, key, scope=scope)
http = httplib2.Http()
http = credentials.authorize(http)
service = build("storage", "v1beta2", http=http)

# res = service.buckets().delete(bucket="test").execute()
# res = service.buckets().list(project="mock_project").execute()
res1 = service.buckets().insert(project="mock_project", body={"name": "test"}).execute()
res2 = service.buckets().get(bucket="test", fields="id").execute()