from collections import namedtuple
from pytest import approx, fixture, raises
from symplyphysics import (
    errors,
    units,
    convert_to,
    Quantity,
    SI,
)
from symplyphysics.laws.kinematic import period_from_angular_frequency as period_def


@fixture(name="test_args")
def test_args_fixture():
    w = Quantity(6.28 * units.radian / units.second)
    Args = namedtuple("Args", ["w"])
    return Args(w=w)


def test_basic_period(test_args):
    result = period_def.calculate_period(test_args.w)
    assert SI.get_dimension_system().equivalent_dims(result.dimension, units.time)
    result_period = convert_to(result, units.second).evalf(2)
    assert result_period == approx(1.0, 0.01)


def test_bad_frequency():
    wb = Quantity(1 * units.meter)
    with raises(errors.UnitsError):
        period_def.calculate_period(wb)
    with raises(TypeError):
        period_def.calculate_period(100)
