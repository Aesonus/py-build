import pytest
from py_build.build import Builder
import logging

@pytest.fixture
def builder():
    return Builder()


def test_mockup_builder(builder: Builder):
    main_output_list = []
    progress_report_list = []
    sub_output_list = []

    def main_step_output(output):
        main_output_list.append(output)

    def sub_step_output(output):
        sub_output_list.append(output)

    def progress_report(progress):
        progress_report_list.append(round(progress * 100))

    step = builder.build_step()
    progress = builder.capture_progress(progress_report)

    output_main_step = builder.capture_results(main_step_output)
    mainstep = builder.composed(step, output_main_step, progress)

    output_sub_step = builder.capture_results(sub_step_output)
    substep = builder.composed(step, progress, output_sub_step)

    @mainstep
    def get_hello():
        """Get the salulation"""
        return "Hello"

    @substep
    def sub_step(out):
        """Get the sub step"""
        return out

    @mainstep
    def get_name(name='Cory'):
        """Get the name"""
        return name

    builder.build([
        None, ('substep',)
    ])

    assert main_output_list == [
        "Hello",
        "Cory"
    ]

    assert progress_report_list == [
        33,
        67,
        100
    ]

    assert sub_output_list == [
        'substep'
    ]