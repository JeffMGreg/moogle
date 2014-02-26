import hashlib

from moogle.core import BaseBackend

from time import strftime, localtime


class BucketAlreadyExists(Exception):
    def __init__(self):
        super(BucketAlreadyExists, self).__init__()

    @property
    def response(self):
        return {
            "error": {
                "errors": [
                    {
                        "domain": "global",
                        "reason": "conflict",
                        "message": "You already own this bucket. Please select another name."
                    }
                ],
                "code": 409,
                "message": "You already own this bucket. Please select another name."
            }
        }


class Project(object):
    def __init__(self, name):
        self.name = name

        owner_hash = hashlib.sha256(name)
        self.owners = owner_hash.hexdigest()

        self.buckets = {}

    def create_bucket(self, name):

        if name in self.buckets:
            raise BucketAlreadyExists
        else:
            bucket = Bucket(self, name)
            self.buckets[name] = bucket
            return bucket


class Bucket(object):
    def __init__(self, project, name):
        self.kind = "storage#bucket"
        self.id = name
        self.selfLink = "https://content.googleapi.com/storage/v1beta2/b/%s" % name
        self.name = name
        self.timeCreated = strftime("%Y-%m-%dT%H:%M:%S.000Z", localtime())
        self.metageneration = 1
        self.owner = {
            "entity": "group-%s" % project.owners,
            "entityId": "%s" % project.owners}
        self.location = "US"
        self.storageClass = "STANDARD"
        self.etag = "CAE="

    def __iter__(self):
        return self.__dict__


class GoogleCloudStorageBackend(BaseBackend):
    def __init__(self):
        self.projects = {}

    def post_bucket(self, bucket_name, project=None):
        project = self.projects.setdefault(project, Project("mock_project"))
        return project.create_bucket(bucket_name)

gcs_backend = GoogleCloudStorageBackend()
