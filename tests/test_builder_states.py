from py_build.build import BuildCompleteState, BuildConfigureState, BuildError, BuildErrorState, BuildRunningState, Builder, BuilderError
import pytest

@pytest.fixture
def builder_configure():
    return Builder(BuildConfigureState)

@pytest.fixture
def builder_complete():
    return Builder(BuildCompleteState)

@pytest.fixture
def builder_running():
    return Builder(BuildRunningState)

@pytest.fixture
def builder_error():
    return Builder(BuildErrorState)

@pytest.fixture
def builder_states(builder_configure, builder_running, builder_complete, builder_error):
    return (builder_configure, builder_running, builder_complete, builder_error)

@pytest.fixture(params=(0, 1, 2))
def builder_running_complete_error(builder_states, request):
    builders = builder_states[1:]
    messages = (
        'Cannot {verb}, build already running',
        'Cannot {verb}, build already completed',
        'Cannot {verb}, build already completed with errors',
    )
    return (builders[request.param], messages[request.param])


def test_build_step_raises_exception_if_builder_running_or_completed(builder_running_complete_error):
    builder, message = builder_running_complete_error
    with pytest.raises(BuilderError, match=message.format(verb='add build step')):
        builder.build_step()


def test_build_raises_exception_if_builder_running_or_completed(builder_running_complete_error):
    builder, message = builder_running_complete_error
    with pytest.raises(BuilderError, match=message.format(verb='run build')):
        builder.build()


@pytest.fixture(params=[
    0, 1
])
def builder_complete_error(builder_states, request):
    return tuple(builder_states[2:])[request.param]


def test_is_complete_returns_true_if_state_is_complete_or_error(builder_complete_error):
    assert builder_complete_error.is_complete == True


@pytest.fixture
def builder():
    return Builder()

def test_build_state_is_running_during_build_step_execution(builder):
    running = []
    @builder.build_step()
    @builder.capture_results(lambda res: running.append(res))
    def assert_state():
        return isinstance(builder.state, BuildRunningState)

    builder.build()
    assert any(running)


def test_build_state_is_complete_when_build_is_complete(builder):
    @builder.build_step()
    def step1():
        pass

    @builder.build_step()
    def step2():
        pass

    builder.build()

    assert isinstance(builder.state, BuildCompleteState)
    assert builder.is_complete


def test_build_state_is_error_when_build_has_exception(builder):
    step3_notran = []
    @builder.build_step()
    def step1():
        pass

    @builder.build_step()
    def errors_step():
        1 / 0

    @builder.build_step()
    @builder.capture_results(lambda res: step3_notran.append(True))
    def step3():
        return True
    exc = None
    with pytest.raises(BuildError):
        try:
            builder.build()
        except BuildError as ex:
            exc = ex
            raise ex
    assert exc.build_step == errors_step
    assert exc.message == 'division by zero'
    assert isinstance(builder.state, BuildErrorState)
    assert builder.is_complete
    assert not any(step3_notran)
