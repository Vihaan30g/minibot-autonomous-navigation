from setuptools import find_packages, setup

import os
from glob import glob

package_name = 'minibot_navigation'

setup(
    name=package_name,
    version='0.0.0',

    packages=find_packages(exclude=['test']),

    data_files=[

        # ament index resource
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name]
        ),

        # package.xml
        (
            'share/' + package_name,
            ['package.xml']
        ),

        # launch files
        (
            os.path.join('share', package_name, 'launch'),
            glob('launch/*.launch.py')
        ),

        # config files
        (
            os.path.join('share', package_name, 'config'),
            glob('config/*.yaml')
        ),

        # rviz files
        (
            os.path.join('share', package_name, 'rviz'),
            glob('rviz/*.rviz')
        ),

        # maps
        (
            os.path.join('share', package_name, 'maps'),
            glob('maps/*')
        ),
    ],

    install_requires=['setuptools'],

    zip_safe=True,

    maintainer='vihaan',

    maintainer_email='vihaan30g@gmail.com',

    description='Navigation, localization, SLAM, and autonomous navigation stack for Minibot.',

    license='Apache License 2.0',

    extras_require={
        'test': ['pytest'],
    },

    entry_points={
        'console_scripts': [
            'odom_logger = minibot_navigation.odom_logger:main',
        ],
    },

)
