from collections import namedtuple
from pytest import approx, fixture, raises
from symplyphysics import (
    errors,
    units,
    Quantity,
    SI,
    convert_to,
)
from symplyphysics.laws.waves import frequency_shift_from_velocity as doppler_law

# Man stands near railroad and hears horn of incoming train. Train comes with velocity of 9km/h and horns with 2000Hz frequency. What frequency hears the man?
## We have online calc for Dopler effect here: https://planetcalc.ru/2351/. With our parameters we should obtain 2015Hz observed frequency.
## Another situation is when man rides a bike towards horning standing train with the same velocity. Observed frequency should be same.


@fixture(name="test_args")
def test_args_fixture():
    sound_velocity = Quantity(340 * units.meter / units.second)
    train_velocity = Quantity(-9 * units.kilometer / units.hour)
    bike_velocity = Quantity(-9 * units.kilometer / units.hour)
    zero_velocity = Quantity(0)
    horn_frequency = Quantity(2000 * units.hertz)
    Args = namedtuple("Args",
        ["sound_velocity", "train_velocity", "bike_velocity", "zero_velocity", "horn_frequency"])
    return Args(sound_velocity=sound_velocity,
        zero_velocity=zero_velocity,
        train_velocity=train_velocity,
        bike_velocity=bike_velocity,
        horn_frequency=horn_frequency)


def test_basic_frequency(test_args):
    result_1 = doppler_law.calculate_observed_frequency(test_args.horn_frequency,
        test_args.sound_velocity, test_args.train_velocity, test_args.zero_velocity)
    result_2 = doppler_law.calculate_observed_frequency(test_args.horn_frequency,
        test_args.sound_velocity, test_args.zero_velocity, test_args.bike_velocity)
    assert SI.get_dimension_system().equivalent_dims(result_1.dimension, units.frequency)
    assert SI.get_dimension_system().equivalent_dims(result_2.dimension, units.frequency)
    result_freq_1 = int(convert_to(result_1, units.hertz).evalf(4))
    assert result_freq_1 == approx(2015, 0.001)
    result_freq_2 = int(convert_to(result_2, units.hertz).evalf(4))
    # Doppler effect is irrelative at relatively low velocities
    assert result_freq_2 == approx(result_freq_1, 0.001)


def test_fast_velocity_frequency(test_args):
    # observer is immobile and emitter is moving
    # speed of sound * 0.8
    object_velocity = Quantity(272 * units.meter / units.second)
    result = doppler_law.calculate_observed_frequency(test_args.horn_frequency,
        test_args.sound_velocity, object_velocity, test_args.zero_velocity)
    assert SI.get_dimension_system().equivalent_dims(result.dimension, units.frequency)
    result_freq = int(convert_to(result, units.hertz).evalf(8))

    # make observer moving and source idle
    result = doppler_law.calculate_observed_frequency(test_args.horn_frequency,
        test_args.sound_velocity, test_args.zero_velocity, object_velocity)
    assert SI.get_dimension_system().equivalent_dims(result.dimension, units.frequency)
    moving_observer_freq = int(convert_to(result, units.hertz).evalf(8))
    # Doppler effect is no longer irrelative at very high velocities
    assert result_freq / moving_observer_freq > 2


def test_bad_velocity(test_args):
    vb = Quantity(1 * units.coulomb)
    with raises(errors.UnitsError):
        doppler_law.calculate_observed_frequency(test_args.horn_frequency, vb,
            test_args.train_velocity, test_args.bike_velocity)
    with raises(TypeError):
        doppler_law.calculate_observed_frequency(test_args.horn_frequency, 100,
            test_args.train_velocity, test_args.bike_velocity)
    with raises(errors.UnitsError):
        doppler_law.calculate_observed_frequency(test_args.horn_frequency, test_args.sound_velocity,
            vb, test_args.bike_velocity)
    with raises(TypeError):
        doppler_law.calculate_observed_frequency(test_args.horn_frequency, test_args.sound_velocity,
            100, test_args.bike_velocity)
    with raises(errors.UnitsError):
        doppler_law.calculate_observed_frequency(test_args.horn_frequency, test_args.sound_velocity,
            test_args.train_velocity, vb)
    with raises(TypeError):
        doppler_law.calculate_observed_frequency(test_args.horn_frequency, test_args.sound_velocity,
            test_args.train_velocity, 100)


def test_bad_frequency(test_args):
    fb = Quantity(1 * units.coulomb)
    with raises(errors.UnitsError):
        doppler_law.calculate_observed_frequency(fb, test_args.sound_velocity,
            test_args.train_velocity, test_args.bike_velocity)
    with raises(TypeError):
        doppler_law.calculate_observed_frequency(100, test_args.sound_velocity,
            test_args.train_velocity, test_args.bike_velocity)
