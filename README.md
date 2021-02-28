# py-build
A package that includes a class for building applications using python

## Usage

The builder uses decorators to designate build steps:

```python
import py_build

# Create the builder object
builder = py_build.Builder()

# Add steps to the builder
@builder.build_step()
def step1():
    return "Output from step 1"

@builder.build_step()
def step2():
    return "Output from step 2"
```

Call each step to run the build:

```python
step1()
step2()
```

## Capturing build step results

The output from build steps (or other processes from inside a build step) can be captured using the ```Builder().capture_results``` decorator method.

This method accepts a list of ```Callable```'s that will be called in the order given with the return value from function decorated.

The following code will print the results from each build step on screen:

```python
import py_build

def output_fnc(output: str):
    print(output)

# Create the builder object
builder = py_build.Builder()

# Add steps to the builder
@builder.build_step()
@builder.capture_results(output_fnc)
def step1():
    return "Output from step 1"

@builder.build_step()
@builder.capture_results(output_fnc)
def step2():
    return "Output from step 2"

step1()
step2()

# Prints:
# Output from step 1
# Output from step 2
```

## Progress Reporting

The progress of the build can be captured as well using the ```Builder().capture_progress``` decorator method. This method accepts a list of ```Callable```'s that accept a ```float``` between ```0``` and ```1```

The following code will print the progress of the build in percentile:

```python
import py_build

def progress_fnc(progress: float):
    print(round(progress * 100))

# Create the builder object
builder = py_build.Builder()

# Add steps to the builder
@builder.build_step()
@builder.capture_progress(progress_fnc)
def step1():
    return "Output from step 1"

@builder.build_step()
@builder.capture_progress(progress_fnc)
def step2():
    return "Output from step 2"

step1()
step2()

# Prints:
# 50
# 100
```

## Composed Decorators

The builder can also combine decorators into a single decorator. This can be useful for preventing repeat code like in the examples above. It can also be used to differentiate main steps from substeps and the like.

The following code will print the results and progress from each step:

```python
import py_build

def progress_fnc(progress: float):
    print(round(progress * 100))

def output_fnc(output: str):
    print(output)

# Create the builder object
builder = py_build.Builder()

main_step = builder.composed(
    @builder.build_step(),
    @builder.capture_progress(progress_fnc),
    @builder.capture_results(output_fnc)
)

# Add steps to the builder
@main_step
def step1():
    return "Output from step 1"

@main_step
def step2():
    return "Output from step 2"

step1()
step2()

# Prints:
# Output from step 1
# 50
# Output from step 2
# 100
```

## The ```Builder().build()``` method

We can also make the builder run steps sequentially with a single method call.

This example does the same thing as the previous example, but uses the ```Builder().build()``` method to execute all the build steps:

```python
import py_build

def progress_fnc(progress: float):
    print(round(progress * 100))

def output_fnc(output: str):
    print(output)

# Create the builder object
builder = py_build.Builder()

main_step = builder.composed(
    @builder.build_step(),
    @builder.capture_progress(progress_fnc),
    @builder.capture_results(output_fnc)
)

# Add steps to the builder
@main_step
def step1():
    return "Output from step 1"

@main_step
def step2():
    return "Output from step 2"

builder.build()

# Prints:
# Output from step 1
# 50
# Output from step 2
# 100
```

There are a few caveats to note about the above example:

+ The ```Builder().build_step()``` must be the first decorator for a function for the example to work correctly
+ Build steps that require arguments should be defined as keyword arguments at definition
+ ```Builder``` instances are callable, so calling ```Builder()()``` is the same as calling ```Builder().build()```.

## Sub steps

The ```Builder().build()``` method can also handle steps that have a sub step. These can be designed as such:

```python
import py_build

def progress_fnc(progress: float):
    print(round(progress * 100))

def output_fnc(output: str):
    print(output)

# Create the builder object
builder = py_build.Builder()

main_step = builder.composed(
    @builder.build_step(),
    @builder.capture_progress(progress_fnc),
    @builder.capture_results(output_fnc)
)

@main_step
def get_hello():
    """Get the salulation"""
    return "Hello"

@main_step
def sub_step():
    new_builder = py_build.Builder()
    substep = new_builder.composed(
        new_builder.build_step(),
        new_builder.capture_progress(progress_fnc), # We will use the same progress reporting method as in main steps
        new_builder.capture_results(output_fnc), # We will use the same result reporting method as in main steps
    )
    @substep
    def sub_step_1():
        """Get the sub step"""
        return "Sub step 1"
    @substep
    def sub_step_2():
        """Get the sub step"""
        return "Sub step 2"
    # Returning a builder object indicates that the step has its own steps
    return new_builder

@main_step
def get_name(name='Cory'):
    """Get the name"""
    return name

builder.build()

# Prints:
# Hello
# 33
# Sub step 1
# 50
# Sub step 2
# 67
# Cory
# 100
```

## Release Notes

There are several changes that may break compatibility between version 0.1.0 and 0.2.0 as outlined below:

+ ```Builder().composed()``` has been renamed to ```Builder().composed_step()``` and its functionality has changed