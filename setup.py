import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

requires = [
    'pyramid',
    'PyBrowserID',
    ]

setup(name='pyramid_persona',
      version='1.0',
      description='pyramid_persona',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        ],
      author='Georges Dubus',
      author_email='georges.dubus@gmail.com',
      url='https://github.com/madjar/pyramid_persona',
      keywords='web pyramid pylons authentication persona',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="pyramid_persona",
      )
