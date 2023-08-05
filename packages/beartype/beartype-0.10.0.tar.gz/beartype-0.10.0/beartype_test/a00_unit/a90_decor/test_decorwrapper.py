#!/usr/bin/env python3
# --------------------( LICENSE                           )--------------------
# Copyright (c) 2014-2022 Beartype authors.
# See "LICENSE" for further details.

'''
**Beartype decorator wrapper function unit tests.**

This submodule unit tests high-level functionality of type-checking wrapper
functions dynamically generated by the :func:`beartype.beartype` decorator.
'''

# ....................{ IMPORTS                           }....................
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# WARNING: To raise human-readable test errors, avoid importing from
# package-specific submodules at module scope.
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
from beartype_test.util.mark.pytskip import skip_if_ci

# ....................{ TESTS ~ fail : obj : large        }....................
# Exclude this test from execution under remote continuous integration (CI)
# workflows. This test's implementation depends on a fixed-duration timeout and
# is thus overly fragile for remote environments not under our control, where
# test execution time is mostly a function of free data center resources.
@skip_if_ci()
def test_wrapper_fail_obj_large() -> None:
    '''
    Test unsuccessful usage of a wrapper function dynamically generated by the
    :func:`beartype.decorator` decorator to type-check a function accepting a
    deeply nested data structure, passed a worst-case structure exposing
    performance regressions in this wrapper function.

    This test guards against regressions in this issue, kindly submitted by
    Cuban type-checking maestro @mvaled (Manuel Vázquez Acosta):

        https://github.com/beartype/beartype/issues/91
    '''

    # Defer heavyweight imports.
    from beartype import beartype
    from beartype.roar import BeartypeCallHintParamViolation
    from beartype.typing import List
    from pytest import raises
    from time import time

    #FIXME: Ideally, this test would gracefully timeout (i.e., report failure
    #after failing to pass for a certain reasonable duration of time).
    #Pragmatically, pytest provides no official means of doing so and, while
    #unofficial pytest plugins purporting to do so do exist (e.g.,
    #"pytest-timeouts"), all of those plugins come with uncomfortable caveats
    #that effectively render any timeouts-based workflow fragile, non-portable,
    #and failure-prone. Instead, we simply test for timeout in the hackiest
    #way possible -- which is why we exclude this test from remote CI hosts.

    # Number of seconds after which the call to the wrapper function defined
    # below passed the worst-called structure defined below is automatically
    # failed. This effectively acts as a poor man's timeout. We are that man.
    TIME_MAX = 15.0

    # Arbitrary callable accepting a deeply nested data structure.
    @beartype
    def behold(the_great_destroyer_of_apps: List[List[List[int]]]) -> int:
        return len(the_great_destroyer_of_apps)

    # Worst-case data structure exposing performance regressions, arbitrarily
    # sized so as to increase the likelihood of this test:
    # * Rapidly passing when the underlying code path is optimized as expected.
    # * Rapidly failing when that path has an unexpected speed regression.
    BAD_APPLE = [[['a']*512]*256]*128

    # Current time in fractional seconds since the UNIX epoch. Begin timing.
    TIME_START = time()

    # Assert this wrapper function raises the expected exception when passed
    # this structure. Since pytest lacks sane facilities for failing tests
    # whose runtime exceeds a reasonable duration (see above), developers are
    # encouraged to manually "fail" this test by inspection at the CLI. *sigh*
    with raises(BeartypeCallHintParamViolation):
        behold(BAD_APPLE)

    # Current time in fractional seconds since the UNIX epoch. End timing.
    TIME_END = time()

    # Total time in fractional seconds consumed by this wrapper function.
    TIME_TOTAL = TIME_END - TIME_START

    # Assert this wrapper function raised this exception within the allotted
    # window of time.
    assert TIME_TOTAL <= TIME_MAX, (
         'Wrapper function "beartype(behold())" failed to type-check '
        f'worst-case input within allotted time duration {TIME_MAX}s.'
    )
