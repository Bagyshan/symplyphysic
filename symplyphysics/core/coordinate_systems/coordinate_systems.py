from enum import Enum, unique
from typing import Optional
from sympy import acos, atan2, cos, sin, sqrt, Expr
from sympy.vector import CoordSys3D, Vector as SymVector
from ..symbols.symbols import next_name


class CoordinateSystem:

    @unique
    class System(Enum):
        CARTESIAN = 0
        CYLINDRICAL = 1
        SPHERICAL = 2

    _coord_system: CoordSys3D
    _coord_system_type: System

    @staticmethod
    def system_to_transformation_name(coord_system_type: System) -> str:
        if coord_system_type == CoordinateSystem.System.CARTESIAN:
            return "cartesian"
        if coord_system_type == CoordinateSystem.System.CYLINDRICAL:
            return "cylindrical"
        if coord_system_type == CoordinateSystem.System.SPHERICAL:
            return "spherical"
        return "none"

    @staticmethod
    def system_to_base_scalars(coord_system_type: System) -> list[str]:
        if coord_system_type == CoordinateSystem.System.CYLINDRICAL:
            return ["r", "theta", "z"]
        if coord_system_type == CoordinateSystem.System.SPHERICAL:
            return ["r", "theta", "phi"]
        return ["x", "y", "z"]

    def __init__(self,
        coord_system_type: System = System.CARTESIAN,
        inner: Optional[CoordSys3D] = None):
        self._coord_system_type = coord_system_type
        if inner is None:
            self._coord_system = CoordSys3D(next_name("CS"),
                variable_names=CoordinateSystem.system_to_base_scalars(coord_system_type))
            return
        self._coord_system = inner

    @property
    def coord_system(self) -> CoordSys3D:
        return self._coord_system

    @property
    def coord_system_type(self) -> System:
        return self._coord_system_type

    def transformation_to_system(self, coord_system_type: System):
        if self._coord_system_type == self.System.CYLINDRICAL:
            r, theta, z = self._coord_system.base_scalars()
            if coord_system_type == self.System.CARTESIAN:
                return (r * cos(theta), r * sin(theta), z)
            if coord_system_type == self.System.CYLINDRICAL:
                return (r, theta, z)

        if self._coord_system_type == self.System.SPHERICAL:
            r, theta, phi = self._coord_system.base_scalars()
            if coord_system_type == self.System.CARTESIAN:
                return (r * sin(theta) * cos(phi), r * sin(theta) * sin(phi), r * cos(theta))
            if coord_system_type == self.System.SPHERICAL:
                return (r, theta, phi)

        if self._coord_system_type == self.System.CARTESIAN:
            x, y, z = self._coord_system.base_scalars()
            if coord_system_type == self.System.CYLINDRICAL:
                return (sqrt(x**2 + y**2), atan2(y, x), z)
            if coord_system_type == self.System.SPHERICAL:
                return (sqrt(x**2 + y**2 + z**2), acos(z / sqrt(x**2 + y**2 + z**2)), atan2(y, x))
            if coord_system_type == self.System.CARTESIAN:
                return (x, y, z)

        coord_name_from = self.system_to_transformation_name(self._coord_system_type)
        coord_name_to = self.system_to_transformation_name(coord_system_type)
        raise ValueError(
            f"Transformation is not supported: from {coord_name_from} to {coord_name_to}")


# Change coordinate system type, eg from cartesian to cylindrical
def coordinates_transform(
    self: CoordinateSystem,
    coord_system_type: CoordinateSystem.System = CoordinateSystem.System.CARTESIAN
) -> CoordinateSystem:
    new_coord_system = self.coord_system.create_new(next_name("C"),
        variable_names=CoordinateSystem.system_to_base_scalars(coord_system_type),
        transformation=None)
    return CoordinateSystem(coord_system_type, new_coord_system)


def coordinates_rotate(self: CoordinateSystem, angle: Expr, axis: SymVector) -> CoordinateSystem:
    if self.coord_system_type != CoordinateSystem.System.CARTESIAN:
        coord_name_from = CoordinateSystem.system_to_transformation_name(self.coord_system_type)
        raise ValueError(
            f"Rotation only supported for cartesian coordinates: got {coord_name_from}")
    return CoordinateSystem(self.coord_system_type,
        self.coord_system.orient_new_axis(next_name("C"), angle, axis))
