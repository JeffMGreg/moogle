__author__ = 'jeff'

from .responses import GCSResponseInstance

url_bases = [
    "https://www.googleapis.com/storage/v1beta2"
]

url_paths = {
    '{0}/b?.+': GCSResponseInstance.bucket_response,
  #  '/(?P<bucket_name>.+)/o/(?P<key_name>.+)/$': GCSResponseInstance.key_response,
}