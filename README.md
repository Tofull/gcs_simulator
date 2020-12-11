# Google Cloud Storage simulator

A simple simulator which allows to use a local folder as "bucket" and try to mimic the `google.cloud.storage` API.

Implemented behaviours:
- `Client`
- `Bucket`
  - `get_blob`
  - `blob`
- `Blob`
  - `download_to_filename`
  - `upload_from_filename`
  - `delete`

## Example

Here is a quick overview how to use this simulator.

```python
from unittest import mock
from gcs_simulator.storage import MockClient

# define a fake client which will replace the google.cloud.storage.Client object.
class FakeClient(MockClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_local_root_folder_used_for_simulation("local_folder_used_by_simulator")


# ...
# and later, use the fake client as follow:

from google.cloud import storage

@mock.patch("google.cloud.storage.Client", FakeClient)
def any_function_which_uses_storage_API():
    # this function will use the mocked Client
    storage_client = storage.Client()

    # retrieve blob
    any_blob = storage_client.bucket("any_bucket").get_blob("any_stored_blob")
    any_blob.download_to_filename("any_local_filename")

    # upload blob
    another_blob = storage_client.bucket("another_bucket").blob("another_blob")
    another_blob.upload_from_filename("any_local_filename")

    # manage blob
    any_blob.delete()
```

See [example folder](./example) to see how to use this simulator with background cloud functions.

# Note for developers

```sh
conda env create --file environment.yml
conda activate gcs_simulator_dev_environment
pre-commit install

python -m pytest
```
