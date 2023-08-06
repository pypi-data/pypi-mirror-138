import numpy as np
import pytest

from hipose.skeleton import Skeleton, SkeletonXsens, \
        SkeletonErgowear, SkeletonMTwAwinda, SkeletonXsensUpper

from hipose.rotations import quat_random

# flake8: noqa: F841

def test_skeleton_objects():

    s1 = Skeleton(root_joint=0, joint_names=["j1", "j2", "j3"],
                  segment_starts=[0, 1], segment_ends=[1, 2])
    s1 = SkeletonXsens()
    s2 = SkeletonMTwAwinda()
    s3 = SkeletonErgowear()
    s4 = SkeletonXsensUpper()


def test_skeleton_mappings():
    # TODO: add
    pass


def test_skeleton_kinematics():
    # TODO: add
    pass


@pytest.mark.filterwarnings("ignore")
@pytest.mark.parametrize("skeleton", [SkeletonXsens(),
                                      SkeletonXsensUpper(),
                                      SkeletonMTwAwinda(),
                                      SkeletonErgowear()])
def test_skeleton_joint_angles(skeleton):
    segs_ori = skeleton.remove_dummy_segments(quat_random(skeleton.num_joints))
    jnt_angles = skeleton.segment_orients_to_relative_joint_angles(
            segs_ori, euler_seq="XYZ", degrees=True
    )
    assert len(jnt_angles) == len(segs_ori)
    assert list(jnt_angles[0]) == [0, 0, 0]


def test_skeleton_vizualization():
    # TODO: add
    pass
