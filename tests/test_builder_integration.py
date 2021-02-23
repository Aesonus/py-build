from pywin_installer.build import Builder
import pytest


def test_mockup_builder():
    output_list = []
    progress_reports = []

    def main_step_output(output):
        output_list.append(output)

    def progress_report(progress):
        progress_reports.append(progress)

    progress = Builder.progress_to(progress_report)
    output_main_step = Builder.output_to(progress(main_step_output))

    @Builder.build_step
    @output_main_step
    def get_hello():
        return "Hello"

    @Builder.build_step
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