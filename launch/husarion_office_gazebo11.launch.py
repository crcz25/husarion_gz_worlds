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

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import EnvironmentVariable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    pkg_share = FindPackageShare("husarion_gz_worlds")
    gazebo_ros_share = FindPackageShare("gazebo_ros")
    models_path = PathJoinSubstitution([pkg_share, "models"])
    world_path = PathJoinSubstitution([pkg_share, "worlds", "husarion_office_gazebo11.world"])

    gazebo_model_path = [
        models_path,
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
            SetEnvironmentVariable("GAZEBO_MODEL_PATH", gazebo_model_path),
            SetEnvironmentVariable("GAZEBO_RESOURCE_PATH", gazebo_resource_path),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    PathJoinSubstitution([gazebo_ros_share, "launch", "gazebo.launch.py"])
                ),
                launch_arguments={
                    "world": world_path,
                    "gui": LaunchConfiguration("gui"),
                    "verbose": LaunchConfiguration("verbose"),
                    "server_required": "true",
                }.items(),
            ),
        ]
    )
