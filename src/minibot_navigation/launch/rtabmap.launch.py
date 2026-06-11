from launch import LaunchDescription
from launch_ros.actions import Node

from ament_index_python.packages import get_package_share_directory

import os


def generate_launch_description():

    pkg_share = get_package_share_directory(
        'minibot_navigation'
    )

    rtabmap_params = os.path.join(
        pkg_share,
        'config',
        'rtabmap.yaml'
    )

    rtabmap_node = Node(
        package='rtabmap_slam',
        executable='rtabmap',
        output='screen',
        parameters=[
            rtabmap_params
        ],
        remappings=[
            ('rgb/image', '/camera/image'),
            ('depth/image', '/camera/depth_image'),
            ('rgb/camera_info', '/camera/camera_info'),
            ('odom', '/odometry/filtered')
        ]
    )

    rtabmap_viz = Node(
        package='rtabmap_viz',
        executable='rtabmap_viz',
        output='screen',
        parameters=[
            {'use_sim_time': True}
        ],
        remappings=[
            ('rgb/image', '/camera/image'),
            ('depth/image', '/camera/depth_image'),
            ('rgb/camera_info', '/camera/camera_info'),
            ('odom', '/odometry/filtered')
        ]
    )

    return LaunchDescription([
        rtabmap_node,
        rtabmap_viz
    ])