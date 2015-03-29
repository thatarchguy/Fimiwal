from setuptools import setup

setup(
    name='fimiwal',
    version='0.0.0a',
    long_description=__doc__,
    packages=['fimiwal'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask>=0.10.0'
    ],
    test_suite='tests'
)
