from pathlib import Path
import tempfile
from typing import Optional
import uuid
import sys

from google.cloud import storage


def demo_background_cloud_function(event, context):
    """
    This background cloud function counts the number of letters in a file.
    A cloud bucket event is expected as input.
    See https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/functions/helloworld/main.py#L89

    Returns:
        None; the output is written to Stackdriver Logging
    """
    storage_client = storage.Client()

    file_name = event["name"]
    bucket_name = event["bucket"]

    with tempfile.TemporaryDirectory() as tmpdirname:
        # generate a random filename in tmpdirname
        local_file = Path(tmpdirname) / str(uuid.uuid4().hex)

        # retrieve the blob object from the bucket, and store it into the local_file
        blob = storage_client.bucket(bucket_name).get_blob(file_name)
        blob.download_to_filename(local_file.as_posix())

        # process the file
        number_of_letters = len(local_file.read_text())
        print(f"{file_name} contains {number_of_letters} letters")


def simulated_cloud_function(event, context, data_path: Optional[Path] = None):
    """
    This function is a wrapper of the background function.

    `data_path` allows giving the function any arbitrary folder as "cloud storage bucket simulator".
    This is useful for pytest and its tmpdir fixture.

    Its default value sets the `data` folder at the root of the repo as the default "cloud storage bucket simulator".

    This function allows developers to use the function-framework very straightforwardly:
    `functions-framework --target=simulated_cloud_function --source=background_cloud_function.py --signature-type=event`
    """
    if data_path is None:  # pragma: no cover
        data_path = Path(__file__).parent / ".." / "data"

    from unittest import mock
    from gcs_simulator.storage import MockClient

    root_folder = Path(data_path).absolute().resolve().as_posix()

    class FakeClient(MockClient):
        """ This allows to mock a "google.cloud.storage.Client" object and use the `root_folder` as bucket simulator
        """

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.set_local_root_folder_used_for_simulation(root_folder)

    @mock.patch("google.cloud.storage.Client", FakeClient)
    def run_function_with_simulator(event, context):
        demo_background_cloud_function(event, context)

    run_function_with_simulator(event, context)


if __name__ == "__main__":
    event = {"name": "simple_txt_file.txt", "bucket": ""}
    simulated_cloud_function(event, None)
