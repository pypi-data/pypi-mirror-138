"""
foobar
~~
Some biocompute
"""

from pathlib import Path

from latch import small_task, workflow
from latch.types import LatchFile


@small_task
def foobar_task(sample_input: LatchFile) -> LatchFile:

    with open(sample_input, "r") as f:
        print(f.read())

    gene = Path("test.fa").resolve()
    with open(gene, "w") as f:
        f.write("> my seq\nAUGAAAAAATTTT")

    return LatchFile(gene, "latch:///test.fa")


@workflow
def foobar(sample_input: LatchFile) -> LatchFile:
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

    """
    return foobar_task(sample_input=sample_input)
