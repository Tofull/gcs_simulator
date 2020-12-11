from pathlib import Path


class MockClient(object):
    def __init__(self):
        pass

    def bucket(self, bucket_name: str):
        return MockBucket(bucket_name)


class MockBucket(object):
    def __init__(self, bucket_name: str):
        self._bucket_path = Path(bucket_name)
        assert self._bucket_path.is_dir()
        assert self._bucket_path.exists()

    def get_blob(self, file_path: str):
        _blob = MockBlob(file_path, bucket_reference=self)
        assert _blob._exists()
        return _blob

    def blob(self, file_path: str):
        _blob = MockBlob(file_path, bucket_reference=self)
        return _blob


class MockBlob(object):
    def __init__(self, file_path: str, bucket_reference: MockBucket):
        self._file_path = file_path
        self._bucket_reference = bucket_reference

    def _get_path(self):
        return self._bucket_reference._bucket_path / self._file_path

    def _exists(self):
        return Path(self._get_path()).exists()

    def download_to_filename(self, local_file_path: str):
        # write content of self._get_path() in local_file_path
        with open(self._get_path(), mode="rb") as blob_content, open(
            local_file_path, mode="wb"
        ) as local_file_content:
            local_file_content.write(blob_content.read())

    def upload_from_filename(self, local_file_path: str):
        # write content of local_file_path in self._get_path()
        self._get_path().parent.mkdir(parents=True, exist_ok=True)
        with open(self._get_path(), mode="wb") as blob_content, open(
            local_file_path, mode="rb"
        ) as local_file_content:
            blob_content.write(local_file_content.read())

    def delete(self):
        self._get_path().unlink()
