from collections import namedtuple
from pytest import approx, fixture, raises
from symplyphysics import (
    errors,
    units,
    convert_to,
    Quantity,
    SI,
)
from symplyphysics.laws.dynamics import kinetic_energy_from_mass_and_velocity as kinetic_energy


@fixture(name="test_args")
def test_args_fixture():
    m = Quantity(0.5 * units.kilogram)
    v = Quantity(0.5 * units.meter / units.second)
    Args = namedtuple("Args", ["m", "v"])
    return Args(m=m, v=v)


def test_basic_kinetic_energy(test_args):
    result = kinetic_energy.calculate_kinetic_energy(test_args.m, test_args.v)
    assert SI.get_dimension_system().equivalent_dims(result.dimension, units.energy)
    result_energy = convert_to(result, units.joule).evalf(3)
    assert result_energy == approx(0.0625, 0.005)


def test_bad_body_mass(test_args):
    bm = Quantity(1 * units.meter)
    with raises(errors.UnitsError):
        kinetic_energy.calculate_kinetic_energy(bm, test_args.v)
    with raises(TypeError):
        kinetic_energy.calculate_kinetic_energy(100, test_args.v)


def test_bad_body_velocity(test_args):
    bv = Quantity(1 * units.meter)
    with raises(errors.UnitsError):
        kinetic_energy.calculate_kinetic_energy(test_args.m, bv)
    with raises(TypeError):
        kinetic_energy.calculate_kinetic_energy(test_args.m, 100)
