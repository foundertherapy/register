from django.contrib.staticfiles.storage import CachedFilesMixin

from pipeline.storage import PipelineMixin, NonPackagingMixin

from storages.backends.s3boto import S3BotoStorage


class NonPackagingS3PipelineCachedStorage(
        NonPackagingMixin, PipelineMixin, CachedFilesMixin, S3BotoStorage):
    location = 'static'
