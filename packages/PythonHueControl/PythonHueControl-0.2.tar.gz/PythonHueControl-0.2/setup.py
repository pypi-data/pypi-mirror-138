from setuptools import setup

setup(
    name='PythonHueControl',
    version='0.2',
    packages=['v1', 'v1.rule', 'v1.group', 'v1.light', 'v1.scene', 'v1.bridge', 'v1.sensor', 'v1.schedule', 'v2'],
    package_dir={'': 'pythonhuecontrol'},
    url='https://github.com/elnkosc/PythonHueControl',
    license='GPL',
    author='Koen',
    author_email='koen@schilders.org',
    description='Feature Rich Python API for Hue V1 and V2'
)
