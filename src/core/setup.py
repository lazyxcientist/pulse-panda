from setuptools import find_packages, setup
import os
from glob import glob
package_name = 'core'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),

        (os.path.join('share', package_name,'srv'), glob('srv/*')),
        (os.path.join('share', package_name,'config'), glob('config/*')),
        (os.path.join('share', package_name,'rviz'), glob('rviz/*')),
        (os.path.join('lib', package_name,'scripts'), glob('scripts/*')),
        (os.path.join('share', package_name,'launch'), glob('launch/*')),
        (os.path.join('share', package_name,'maps'), glob('maps/*')),
        (os.path.join('share', package_name,'world'), glob('world/*')),

        (os.path.join('share', package_name,'xparo/aiml'), glob('xparo/aiml/*')),
        (os.path.join('share', package_name,'xparo/sets'), glob('xparo/sets/*')),
        (os.path.join('share', package_name,'xparo/maps'), glob('xparo/maps/*')),
        (os.path.join('share', package_name,'xparo/properties'), glob('xparo/properties/*')),
        (os.path.join('share', package_name,'xparo/speak'), glob('xparo/speak/*')),
        

    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='scientist',
    maintainer_email='xpscientist@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)
