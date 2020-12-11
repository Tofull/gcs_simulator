from pathlib import Path


class MockClient(object):
    def __init__(self):
        self._root_folder = None

    def set_local_root_folder_used_for_simulation(self, root_folder: str):
        assert Path(root_folder).is_dir()
        assert Path(root_folder).exists()
        self._root_folder = root_folder

    def _requires_root_folder(fn):
        def _validate_root_folder(self, *args, **kwargs):
            if self._root_folder is None:
                raise RuntimeError(
                    "Missing required root folder to use the Google Storage simulator. "
                    "Please call `set_local_root_folder_used_for_simulation('any_local_folder_path')` "
                    "to use the folder 'any_local_folder_path' as a root for the Google Storage simulator."
                )
            return fn(self, *args, **kwargs)

        return _validate_root_folder

    @_requires_root_folder
    def bucket(self, bucket_name: str):
        return MockBucket(bucket_name, root_folder=self._root_folder)


class MockBucket(object):
    def __init__(self, bucket_name: str, root_folder: str):
        self._bucket_path = Path(root_folder) / bucket_name
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
