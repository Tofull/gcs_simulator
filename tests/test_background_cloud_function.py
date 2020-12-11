from pathlib import Path

from example.background_cloud_function import simulated_cloud_function

from .common import get_files


def test_cloud_function_zip_format(default_bucket_structure, capsys):
    (
        ROOT_FOLDER,
        SOURCE_BUCKET_FOLDER,
        DESTINATION_BUCKET_FOLDER,
    ) = default_bucket_structure

    relative_txt_file = "simple_txt_file.txt"

    # ensure default_bucket_structure fixture does its job
    assert Path(ROOT_FOLDER).exists()
    assert Path(SOURCE_BUCKET_FOLDER).exists()
    assert Path(DESTINATION_BUCKET_FOLDER).exists()
    assert len(get_files(DESTINATION_BUCKET_FOLDER)) == 0
    assert (Path(SOURCE_BUCKET_FOLDER) / relative_txt_file).exists()

    # given
    event = {"name": relative_txt_file, "bucket": SOURCE_BUCKET_FOLDER}
    context = None
    data_path = ROOT_FOLDER

    # when
    simulated_cloud_function(event, context, data_path=data_path)

    # then
    captured = capsys.readouterr()
    assert captured.out == "simple_txt_file.txt contains 8 letters\n"
