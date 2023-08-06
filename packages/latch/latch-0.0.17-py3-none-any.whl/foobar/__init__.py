"""
foobar
~~
Some biocompute
"""

from flytekit.types.directory import FlyteDirectory
from flytekit.types.file import FlyteFile
from latch import small_task, workflow


@small_task()
def foobar_task(sample_input: FlyteFile, output_dir: FlyteDirectory) -> str:
    return "foo"


@workflow
def foobar(sample_input: FlyteFile, output_dir: FlyteDirectory) -> str:
    """Description...

    foobar markdown
    ----

    Write some documentation about your workflow in
    markdown here:

    > Markdown syntax works as expected.

    ## Foobar

    __metadata__:
        display_name: foobar
        author:
            name: n/a
            email:
            github:
        repository:
        license:
            id: MIT

    Args:

        sample_input:
          A description

          __metadata__:
            display_name: Sample Param

        output_dir:
          A description

          __metadata__:
            display_name: Output Directory
    """
    return foobar_task(sample_input=sample_input, output_dir=output_dir)
