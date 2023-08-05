from setuptools import setup, find_packages


setup(
    name='samplebro',
    version='0.1',
    license='MIT',
    author="Sicepatkilat",
    author_email='sicepatkilat21@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/Deploybotdotcom/pypi',
    keywords='Master Project',
    install_requires=[
          'scikit-learn',
      ],

)
