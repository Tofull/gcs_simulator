from pathlib import Path
import filecmp

import pytest

from gcs_simulator.storage import MockClient

from .common import get_files


def test_gcs_simulator_requires_root_path(default_bucket_structure):
    (
        ROOT_FOLDER,
        SOURCE_BUCKET_FOLDER,
        DESTINATION_BUCKET_FOLDER,
    ) = default_bucket_structure

    with pytest.raises(RuntimeError) as excinfo:
        storage_client = MockClient()
        source_bucket = storage_client.bucket("bucket_source")
    assert "Missing required root folder to use the Google Storage simulator." in str(
        excinfo.value
    )


def test_gcs_simulator(default_bucket_structure, tmpdir, get_simple_txt_file):
    (
        ROOT_FOLDER,
        SOURCE_BUCKET_FOLDER,
        DESTINATION_BUCKET_FOLDER,
    ) = default_bucket_structure

    # ensure default_bucket_structure fixture does it job
    assert len(get_files(SOURCE_BUCKET_FOLDER)) == 1
    assert len(get_files(DESTINATION_BUCKET_FOLDER)) == 0

    # simulate storage client connexion
    storage_client = MockClient()
    storage_client.set_local_root_folder_used_for_simulation(ROOT_FOLDER)

    source_bucket = storage_client.bucket("bucket_source")
    destination_bucket = storage_client.bucket("bucket_destination")

    # try downloading a blob object from the source bucket to a local file
    source_blob = source_bucket.get_blob("simple_txt_file.txt")
    tmp_local_file = str(tmpdir.join("copy_simple_txt_file.txt"))
    source_blob.download_to_filename(tmp_local_file)

    # ensure downloaded file is the same than original file
    assert filecmp.cmp(str(tmp_local_file), str(get_simple_txt_file))

    # try uploading a local file to the destination bucket
    destination_blob = destination_bucket.blob("uploaded_simple_txt_file.txt")
    destination_blob.upload_from_filename(tmp_local_file)

    # ensure uploaded blob object is the same than original file, with its new blob name
    assert len(get_files(DESTINATION_BUCKET_FOLDER)) == 1
    uploaded_file = get_files(DESTINATION_BUCKET_FOLDER)[0]
    assert filecmp.cmp(str(uploaded_file), str(get_simple_txt_file))
    assert uploaded_file.name == "uploaded_simple_txt_file.txt"

    # try deleting the blob from source bucket
    source_blob.delete()
    assert len(get_files(SOURCE_BUCKET_FOLDER)) == 0
