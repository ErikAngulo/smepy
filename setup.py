from setuptools import setup

setup(
   name='smepy',
   version='0.3.0',
   author='Erik Angulo',
   author_email='eangulo014@ikasle.ehu.eus',
   packages=['smepy', 'smepy.test'],
   url='https://github.com/erikangulo/smepy',
   license='LICENSE.txt',
   description='Easy-to-use dataframe statistical analysis',
   long_description=open('README.txt').read(),
   tests_require=['pytest'],
   install_requires=[
      "seaborn >= 0.9.0",
      "pandas >= 0.25.1",
      "matplotlib >= 3.1.1",
      "numpy >=1.17.2"
   ],
)
