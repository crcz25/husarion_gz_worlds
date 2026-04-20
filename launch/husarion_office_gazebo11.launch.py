#!/usr/bin/env python3

# Copyright 2026 Husarion sp. z o.o.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import EnvironmentVariable, LaunchConfiguration


def generate_launch_description():
    pkg_share = get_package_share_directory("husarion_gz_worlds")
    gazebo_ros_share = get_package_share_directory("gazebo_ros")
    turtlebot3_gazebo_share = get_package_share_directory("turtlebot3_gazebo")
    turtlebot3_launch_dir = os.path.join(turtlebot3_gazebo_share, "launch")

    world_path = os.path.join(pkg_share, "worlds", "husarion_office_gazebo11.world")
    husarion_models_path = os.path.join(pkg_share, "models")
    turtlebot3_models_path = os.path.join(turtlebot3_gazebo_share, "models")

    use_sim_time = LaunchConfiguration("use_sim_time")
    x_pose = LaunchConfiguration("x_pose")
    y_pose = LaunchConfiguration("y_pose")
    yaw = LaunchConfiguration("yaw")

    gazebo_model_path = [
        husarion_models_path,
        os.pathsep,
        turtlebot3_models_path,
        os.pathsep,
        EnvironmentVariable("GAZEBO_MODEL_PATH", default_value=""),
    ]
    gazebo_resource_path = [
        pkg_share,
        os.pathsep,
        EnvironmentVariable("GAZEBO_RESOURCE_PATH", default_value=""),
    ]

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "gui",
                default_value="true",
                description="Set to false to run gzserver without gzclient.",
            ),
            DeclareLaunchArgument(
                "verbose",
                default_value="false",
                description="Set to true to increase Gazebo Classic log output.",
            ),
            DeclareLaunchArgument(
                "use_sim_time",
                default_value="true",
                description="Use simulation time.",
            ),
            DeclareLaunchArgument(
                "x_pose",
                default_value="0.6",
                description="Initial x position of the TurtleBot3 robot.",
            ),
            DeclareLaunchArgument(
                "y_pose",
                default_value="0.0",
                description="Initial y position of the TurtleBot3 robot.",
            ),
            DeclareLaunchArgument(
                "yaw",
                default_value="-1.57",
                description="Initial yaw of the TurtleBot3 robot in radians.",
            ),
            SetEnvironmentVariable("GAZEBO_MODEL_PATH", gazebo_model_path),
            SetEnvironmentVariable("GAZEBO_RESOURCE_PATH", gazebo_resource_path),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(gazebo_ros_share, "launch", "gazebo.launch.py")
                ),
                launch_arguments={
                    "world": world_path,
                    "gui": LaunchConfiguration("gui"),
                    "verbose": LaunchConfiguration("verbose"),
                    "server_required": "true",
                }.items(),
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(turtlebot3_launch_dir, "robot_state_publisher.launch.py")
                ),
                launch_arguments={"use_sim_time": use_sim_time}.items(),
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(turtlebot3_launch_dir, "spawn_turtlebot3.launch.py")
                ),
                launch_arguments={"x_pose": x_pose, "y_pose": y_pose, "yaw": yaw}.items(),
            ),
        ]
    )
