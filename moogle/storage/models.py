import hashlib

from moogle.core import BaseBackend
from moogle.storage.errors import *

from time import strftime, localtime


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

    def delete_bucket(self, name):

        bucket = self.buckets.get(name, False)
        if not bucket:
            raise BucketNotFound

        if len(bucket) != 0:
            raise BucketNotEmpry

        elif (len(bucket) == 0) and (name in self.buckets):
            self.buckets.pop[name]
            return None

        else:
            raise BucketNotFound

    def list_buckets(self):

        return self.buckets.values()

    def get_bucket(self, name):

        bucket = self.buckets.get(name)
        if bucket:
            return bucket
        else:
            raise BucketNotFound


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

        self.visible_fields = map(lambda x: "show_%s" % x, self.__dict__.keys())

    def __iter__(self):
        return self.__dict__


class GoogleCloudStorageBackend(BaseBackend):
    def __init__(self):
        self.projects = {"mock_project": Project("mock_project")}

    def post_bucket(self, bucket_name, project="mock_project"):
        project = self.projects.setdefault(project, Project(project))
        return project.create_bucket(bucket_name)

    def get_bucket(self, bucket_name, project="mock_project"):
        project = self.projects[project]
        return project.get_bucket(bucket_name)

    def list_buckets(self, project="mock_project"):
        project = self.projects[project]
        return project.list_buckets()

    def delete_bucket(self, bucket_name, project="mock_project"):
        project = self.projects[project]
        return project.delete_bucket(bucket_name)


gcs_backend = GoogleCloudStorageBackend()
