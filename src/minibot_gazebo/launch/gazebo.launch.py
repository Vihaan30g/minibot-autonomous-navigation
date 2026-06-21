



"""
minibot Ignition Gazebo simulation launch file.

Key fixes vs the original:
  1. Consolidated ros_gz_bridge — Clock, IMU, and Camera topics are routed through
     a single node reading from bridge_config.yaml.
  2. Controller spawners are given use_sim_time:=true so they honour sim time.
  3. A topic relay is added to forward /cmd_vel → the actual controller topic
     /diff_drive_controller/cmd_vel_unstamped, replacing the broken
     <ros><remapping> inside the URDF plugin tag.
  4. Timer periods are tuned conservatively so Ignition is fully ready before
     the robot is spawned and controllers are loaded.
"""

import os
import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction
from launch_ros.actions import Node


def generate_launch_description():

    pkg_path = get_package_share_directory('minibot_description')
    urdf_path = os.path.join(pkg_path, 'urdf', 'minibot.urdf.xacro')

    pkg_minibot_gazebo = get_package_share_directory('minibot_gazebo')
    bridge_config = os.path.join(pkg_minibot_gazebo, 'config', 'bridge_config.yaml')

    controller_config = os.path.join(
        get_package_share_directory('minibot_control'),
        'config',
        'controllers.yaml'
    )

    robot_description_config = xacro.process_file(urdf_path)
    robot_description = robot_description_config.toxml()

    # world_path = os.path.join(
    #     get_package_share_directory('minibot_gazebo'),
    #     'worlds',
    #     'minibot_world.sdf'
    # )

    world_path = "/home/marsuser/.ignition/fuel/tugbot_depot/tugbot_depot.sdf"
 
    return LaunchDescription([

        # ── 1. IGNITION GAZEBO ──────────────────────────────────────────────
        ExecuteProcess(
            cmd=['ign', 'gazebo', world_path, '-r'],
            output='screen'
        ),

        # ── 2. CONSOLIDATED PARAMETER BRIDGE ────────────────────────────────
        # Bridges /clock, /imu, /camera topics altogether from one config file.
        # This keeps our resource footprints low and manages timing cleanly.
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            name='ros_gz_parameter_bridge',
            parameters=[{'config_file': bridge_config}],
            output='screen'
        ),

        # ── 3. ROBOT STATE PUBLISHER ────────────────────────────────────────
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[
                {'robot_description': robot_description},
                {'use_sim_time': True},
            ]
        ),

        # ── 4. SPAWN ROBOT ──────────────────────────────────────────────────
        # Give Ignition 4 s to initialise before spawning.
        TimerAction(
            period=4.0,
            actions=[
                Node(
                    package='ros_gz_sim',
                    executable='create',
                    name='spawn_minibot',
                    arguments=[
                        '-topic', 'robot_description',
                        '-name',  'minibot',
                    ],
                    output='screen'
                ),
            ]
        ),

        # ── 5. JOINT STATE BROADCASTER ──────────────────────────────────────
        # Wait for the robot to be fully loaded in Ignition before starting
        # the controller manager controllers.
        TimerAction(
            period=8.0,
            actions=[
                Node(
                    package='controller_manager',
                    executable='spawner',
                    name='joint_state_broadcaster_spawner',
                    # pass use_sim_time so the spawner uses the bridged clock
                    arguments=[
                        'joint_state_broadcaster',
                        '--controller-manager', '/controller_manager',
                        '--controller-manager-timeout', '30',
                    ],
                    parameters=[{'use_sim_time': True}],
                    output='screen'
                ),
            ]
        ),

        # ── 6. DIFF DRIVE CONTROLLER ────────────────────────────────────────
        TimerAction(
            period=10.0,
            actions=[
                Node(
                    package='controller_manager',
                    executable='spawner',
                    name='diff_drive_controller_spawner',
                    arguments=[
                        'diff_drive_controller',
                        '--controller-manager', '/controller_manager',
                        '--controller-manager-timeout', '30',
                        '--param-file',
                        controller_config,
                    ],
                    parameters=[{'use_sim_time': True}],
                    output='screen'
                ),
            ]
        ),

        # ── 7. CMD_VEL RELAY ────────────────────────────────────────────────
        # The diff_drive_controller with use_stamped_vel=false listens on
        # /diff_drive_controller/cmd_vel_unstamped, NOT /cmd_vel.
        # This relay lets you publish to /cmd_vel (the standard Nav2 / teleop
        # topic) and forwards it transparently to the controller.
        TimerAction(
            period=11.0,   # start after the controller is active
            actions=[
                Node(
                    package='topic_tools',
                    executable='relay',
                    name='cmd_vel_relay',
                    arguments=[
                        '/cmd_vel',
                        '/diff_drive_controller/cmd_vel_unstamped',
                    ],
                    parameters=[{'use_sim_time': True}],
                    output='screen'
                ),
            ]
        ),

    ])