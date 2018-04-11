from setuptools import setup

setup(
    name='LSM',
    version='0.1',
    packages=['lsm'],
    install_requires=[
        'psutil==5.4.3',
        'prettytable',
        'python-crontab'
    ],
    url='https://github.com/EgorLu/lsm',
    license='MIT',
    author='Egor Lunin',
    author_email='elunin@infinidat.com',
    description='Light System Monitor'
)
