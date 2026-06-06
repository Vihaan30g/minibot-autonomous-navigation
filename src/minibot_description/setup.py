from setuptools import setup
import os
from glob import glob

package_name = 'minibot_description'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[

        ('share/' + package_name, ['package.xml']),

        (os.path.join('share', package_name, 'launch'),
            glob('launch/*.py')),

        (os.path.join('share', package_name, 'urdf'),
            glob('urdf/*')),

        (os.path.join('share', package_name, 'rviz'),
            glob('rviz/*')),

    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Vihaan',
    maintainer_email='vihaan@gmail.com',
    description='MiniBot description package',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [],
    },
)

