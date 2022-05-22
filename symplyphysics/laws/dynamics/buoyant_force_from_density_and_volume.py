from symplyphysics import (
    symbols, Eq, pretty, solve, Quantity, units,
    validate_input, validate_output, expr_to_quantity
)

# Description
## Any object, totally or partially immersed in a fluid or liquid, is buoyed up by a force equal to the
## weight of the fluid displaced by the object. Also known as Archimedes principle. Buoyant force
## vector goes against gravity vector.

## Law: Fa = ⍴ * g * V
## Where:
## Fa - buoyant (Archimedes) force.
## ⍴ - density of the fluid.
##   See [material density](symplyphysics/definitions/density_from_mass_volume.py) implementation.
## g - gravity acceleration constant.
## V - volume of the displaced fluid.

force_buoyant, material_density, displaced_volume = symbols('force_buoyant material_density displaced_volume')
law = Eq(force_buoyant, material_density * units.acceleration_due_to_gravity * displaced_volume)

def print():
    return pretty(law, use_unicode=False)

@validate_input(material_density_=(units.mass / units.volume), displaced_volume_=units.volume)
@validate_output(units.force)
def calculate_force_buoyant(material_density_: Quantity, displaced_volume_: Quantity) -> Quantity:
    result_force_expr = solve(law, force_buoyant, dict=True)[0][force_buoyant]
    result_expr = result_force_expr.subs({material_density: material_density_, displaced_volume: displaced_volume_})
    return expr_to_quantity(result_expr, 'force_buoyant')
