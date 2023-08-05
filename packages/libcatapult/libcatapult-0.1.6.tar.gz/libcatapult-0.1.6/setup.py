
from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

with open('requirements.txt') as requirements_file:
    requirements = [line.rstrip('\n') for line in requirements_file]

with open('requirements-test.txt') as requirements_test_file:
    requirements_test = [line.rstrip('\n') for line in requirements_test_file]

setup(
    author='Emily Selwood',
    author_email='emily.selwood@sa.catapult.org.uk',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
    ],
    description='A library of useful code for use in the catapult',
    long_description=readme + '\n\n' + history,
    long_description_content_type="text/markdown",
    version='0.1.6',
    keywords='catapult library',
    name='libcatapult',
    license='apache2',
    packages=find_packages(),
    install_requires=requirements,
    setup_requires=["wheel"],
    tests_require=requirements_test,
    test_suite='nose2.collector.collector',
    url='https://github.com/SatelliteApplicationsCatapult/libcatapult',
)
