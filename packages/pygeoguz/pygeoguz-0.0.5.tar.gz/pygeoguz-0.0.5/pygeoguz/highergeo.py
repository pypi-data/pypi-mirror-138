import math

from .objects import PointBL, LineBL
from .simplegeo import true_angle


def pgz_spherical(latitude, longitude, line_spherical: LineBL):
    phi_1 = math.radians(latitude)
    lambda_1 = math.radians(longitude)
    alpha_1 = math.radians(line_spherical.direction)
    sigma = math.radians(line_spherical.length)

    sin_phi_2 = math.sin(phi_1) * math.cos(sigma) + math.cos(phi_1) * math.sin(
        sigma
    ) * math.cos(alpha_1)

    alpha_2 = math.atan2(
        (math.cos(phi_1) * math.cos(alpha_1)),
        (
            math.cos(phi_1) * math.cos(sigma) * math.cos(alpha_1)
            - math.sin(phi_1) * math.sin(sigma)
        ),
    )

    delta_lambda = math.atan2(
        math.sin(sigma) * math.sin(alpha_1),
        math.cos(phi_1) * math.cos(sigma)
        - sin_phi_2 * math.sin(sigma) * math.sin(alpha_1),
    )
    lambda_2 = lambda_1 + delta_lambda

    true_phi_2 = math.degrees(math.asin(sin_phi_2))
    true_alpha_2 = true_angle(math.degrees(alpha_2), 360)
    true_lambda_2 = true_angle(math.degrees(lambda_2), 360)

    return PointBL(true_phi_2, true_lambda_2), LineBL(
        line_spherical.length, true_alpha_2
    )
