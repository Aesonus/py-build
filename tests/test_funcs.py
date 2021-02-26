import pytest
from py_build.funcs import print_step_doc, print_step_name

@pytest.fixture(params=[
    (),
    ('*',)
])
def step_name_args(request):
    return request.param


def test_print_step_name_outputs_the_step_name(capsys: pytest.CaptureFixture, step_name_args):
    def test_fnc():
        pass
    print_step_name(args=step_name_args)(test_fnc)()
    actual = capsys.readouterr().out.strip()
    assert actual == 'Test{}fnc'.format(
        step_name_args[0] if len(step_name_args) > 0 else ' '
    )

def test_print_step_doc_outputs_the_step_doc(capsys: pytest.CaptureFixture):
    def test_fnc():
        """Test Doc"""
    print_step_doc()(test_fnc)()
    actual = capsys.readouterr().out.strip()
    assert actual == 'Test Doc'