import pytest
from py_build.build import Builder


@pytest.fixture
def builder():
    return Builder()


@pytest.fixture
def assertive_build_steps(builder):
    @builder.build_step
    def step1(arg, kw=None):
        """Step 1"""
        assert arg and kw

    @builder.build_step
    def step2(arg, arg2, kw=None, kw2=None):
        """Step 2"""
        assert arg and arg2 and kw and kw2

    return (step1, step2)


def test_build_step_count(builder, assertive_build_steps):
    assert builder.steps == 2


def test_build_step_gets_the_args(assertive_build_steps):
    step1, step2 = assertive_build_steps
    step1(True, kw=True)
    step2(True, True, kw=True, kw2=True)


@pytest.fixture
def build_steps(builder):
    @builder.build_step
    def step1(returns):
        return returns

    @builder.build_step
    def step2(returns):
        return returns

    return (step1, step2)


def test_build_steps_update_executed_steps(builder, build_steps):
    step1, step2 = build_steps
    step1(True)
    assert builder.executed_steps == 1
    step2(True)
    assert builder.executed_steps == 2


def test_output_to_returns_function_return_to_given_functions(builder, build_steps):
    class Test:
        called = False

        @classmethod
        def output_fnc(cls, output):
            cls.called = True
            assert output

    step1, step2 = [builder.output_to(Test.output_fnc)(step)
                    for step in build_steps]

    step1(True)
    step2('Yess')
    assert builder.steps == 2
    assert Test.called


def test_progress_to_returns_step_progress_to_given_functions(builder, build_steps):
    class Test:
        called = 0
        expects = [0.5, 1]

        @classmethod
        def progress_fnc(cls, output):
            assert output == cls.expects[cls.called]
            cls.called += 1

    step1, step2 = [builder.progress_to(
        Test.progress_fnc)(step) for step in build_steps]

    step1(True)
    step2('Yess')
    assert builder.steps == 2
    assert Test.called == 2
