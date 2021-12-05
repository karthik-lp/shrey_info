from math import ceil, sqrt
from tf.transformations import quaternion_from_euler, euler_from_quaternion
from geometry_msgs.msg import Quaternion
import numpy as np


def quat_to_yaw(q):
    if isinstance(q, Quaternion):
        quat = (q.x, q.y, q.z, q.w)
    elif isinstance(q, np.ndarray):
        quat = (q[0], q[1], q[2], q[3])
    else:
        raise ValueError(
            f"Quaternion given should be of type: np.ndarray or geometry_msgs. \
                Quaternion Given: {type(q)}"
        )
    return euler_from_quaternion(quat)[2]


def yaw_to_quat(yaw):
    return Quaternion(
        **dict(zip(["x", "y", "z", "w"], quaternion_from_euler(0, 0, yaw)))
    )


def rotate_quat(quat, theta):
    if isinstance(quat, Quaternion):
        q = (quat.x, quat.y, quat.z, quat.w)
        euler = euler_from_quaternion(q)
        yaw = euler[2] + theta
        return quaternion_from_euler(0, 0, yaw)
    elif isinstance(quat, dict):
        q = (quat["x"], quat["y"], quat["z"], quat["w"])
        euler = euler_from_quaternion(q)
        yaw = euler[2] + theta
        return dict(zip(["x", "y", "z", "w"], quaternion_from_euler(0, 0, yaw)))
    else:
        raise ValueError(
            f"Quaternion given should be of type: dict or geometry_msgs. \
                Quaternion Given: {type(quat)}"
        )


def diagonal_of_rectangle(width, height):
    """diagonal_of_rectangle
    A simple calculation to get the maximal diagonal(rounded up). This holds for for normal rectangles

    :param width: The width of the rectangle
    :type width: int
    :param height: The height of the rectangle
    :type height: int
    :return: The length of the diagonal as int
    :rtype: diagonal
    """
    diagonal = sqrt(width ** 2 + height ** 2)
    return ceil(diagonal)
