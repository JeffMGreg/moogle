__author__ = 'jeff'

from .responses import BucketResponse, ObjectResponse

url_bases = [
    "https://www.googleapis.com/storage/v1beta2"
]

url_paths = {
    '{0}/b?.*': BucketResponse.bucket_response,
    '{0}/b/test/o/.*?.*': ObjectResponse.object_response,
    'https://www.googleapis.com/upload/storage/v1beta2/b/test/o?.*': ObjectResponse.object_response,
}