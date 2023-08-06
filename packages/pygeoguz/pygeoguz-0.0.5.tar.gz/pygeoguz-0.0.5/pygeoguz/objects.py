from dataclasses import dataclass, field
import math


@dataclass
class Point2D:
    """
    Точка в плоской прямоугольной системе координат (XY)
    """

    x: float
    y: float
    name: str = "default"


@dataclass
class Point3D:
    """
    Точка в пространственной прямоугольной системе координат (XYZ)
    """

    x: float
    y: float
    z: float
    name: str = "default"


@dataclass
class PointBL:
    """
    Точка в геодезической системе координат (BL)
    """

    b: float
    l: float
    name: str = "default"


@dataclass
class Line2D:
    length: float
    direction: float
    name: str = "default"


@dataclass
class LineBL:
    length: float
    direction: float
    name: str = "default"


@dataclass
class Angle:
    degrees: int
    minutes: int
    seconds: float
    name: str = "default"


class Ellipsoid:
    def __init__(self, equatorial_radius, flattering):
        self._equatorial_radius = equatorial_radius
        self._flattering = flattering
        self._polar_radius = (
            -self._equatorial_radius / self._flattering + self._equatorial_radius
        )

    def __repr__(self):
        return f"Ellipsoid(equatorial_radius={self._equatorial_radius}, polar_radius={self._polar_radius})"

    @property
    def equatorial_radius(self):
        return self._equatorial_radius

    @property
    def polar_radius(self):
        return self._polar_radius

    @property
    def flattering(self):
        return self._flattering

    def eccentricity(self):
        e = (
            math.sqrt(self._equatorial_radius ** 2 - self._polar_radius ** 2)
            / self._equatorial_radius
        )
        return e

    def second_eccentricity(self):
        e = (
            math.sqrt(self._equatorial_radius ** 2 - self._polar_radius ** 2)
            / self._polar_radius
        )
        return e

    def square(self):
        a = self._equatorial_radius
        b = self._polar_radius
        s = (
            2
            * math.pi
            * a
            * (
                a
                + b ** 2
                / math.sqrt(a ** 2 - b ** 2)
                * math.log((a + math.sqrt(a ** 2 - b ** 2)) / b)
            )
        )
        return s

    def volume(self):
        v = 4 / 3 * math.pi * self._equatorial_radius ** 2 * self._polar_radius
        return v

    def calculate_ellipsoid(self):
        return {
            "equatorial_radius": self._equatorial_radius,
            "polar_radius": self._polar_radius,
            "flattering": self._flattering,
            "eccentricity": self.eccentricity(),
            "second_eccentricity": self.second_eccentricity(),
            "square": self.square(),
            "volume": self.volume(),
        }
