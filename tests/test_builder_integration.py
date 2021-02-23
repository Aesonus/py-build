import pytest
from py_build.build import Builder


@pytest.fixture
def builder():
    return Builder()


def test_mockup_builder(builder):
    output_list = []
    progress_reports = []

    def main_step_output(output):
        output_list.append(output)

    def progress_report(progress):
        progress_reports.append(progress)

    progress = builder.progress_to(progress_report)
    output_main_step = builder.output_to(progress(main_step_output))

    @builder.build_step
    @output_main_step
    def get_hello():
        return "Hello"

    @builder.build_step
    @output_main_step
    def get_name(name=None):
        return name

    get_hello()
    get_name(name='Cory')

    assert output_list == [
        "Hello",
        "Cory"
    ]

    assert progress_reports == [
        0.5,
        1
    ]
