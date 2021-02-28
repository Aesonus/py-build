import pytest
from py_build.build import Builder

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

    progress = builder.capture_progress(progress_report)

    output_main_step = builder.capture_results(main_step_output)
    mainstep = builder.composed_step(output_main_step, progress)

    output_sub_step = builder.capture_results(sub_step_output)
    substep = builder.composed_step(progress, output_sub_step)

    @mainstep
    def get_hello():
        """Get the salulation"""
        return "Hello"

    @substep
    def sub_step():
        """Get the sub step"""
        return 'substep'

    @mainstep
    def get_name(name='Cory'):
        """Get the name"""
        return name

    builder.build()

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

### v0.2.0: New tests to satisfy sub stages requirements


def test_build_with_substeps(builder: Builder):
    main_output_list = []
    progress_report_list = []

    def main_step_output(output):
        main_output_list.append(output)

    def progress_report(progress):
        progress_report_list.append(round(progress * 100))

    progress = builder.capture_progress(progress_report)

    output_main_step = builder.capture_results(main_step_output)
    step = builder.composed_step(output_main_step, progress)

    @step
    def get_hello():
        """Get the salulation"""
        return "Hello"

    @step
    def sub_step():
        new_builder = Builder()
        substep = new_builder.composed_step(
            new_builder.capture_results(main_step_output),
            new_builder.capture_progress(progress_report))
        @substep
        def sub_step_1():
            """Get the sub step"""
            return "Sub step 1"
        @substep
        def sub_step_2():
            """Get the sub step"""
            return "Sub step 2"
        return new_builder


    @step
    def get_name(name='Cory'):
        """Get the name"""
        return name

    builder.build()
    assert ['Hello', 'Sub step 1', 'Sub step 2', 'Cory'] == main_output_list
    assert [33, 50, 67, 100] == progress_report_list