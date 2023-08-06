import pytest
import hypothesis.strategies as st
from hypothesis import given, settings

from _assembly.lib.util.time import nanoseconds_to_isoformat, isoformat_to_milliseconds


st_integers = st.integers(min_value=int(1e9), max_value=13569465600 * int(1e9))


@settings(deadline=None)
@pytest.mark.proptest
@given(ns=st_integers)
def test_timestamp_conversion(ns):
    ms = ns // int(1e6)
    assert isoformat_to_milliseconds(nanoseconds_to_isoformat(ns)) == ms
