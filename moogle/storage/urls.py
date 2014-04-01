__author__ = 'jeff'

from .responses import response

url_bases = [
    "https://www.googleapis.com/storage/v1beta2"
]

url_paths = {
    '{0}.*': response,
    'https://www.googleapis.com/upload/storage/v1beta2/': response,
}