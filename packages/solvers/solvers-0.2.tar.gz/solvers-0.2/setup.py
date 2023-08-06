from setuptools import setup, find_packages


setup(
    name='solvers',
    version='0.2',
    license='MIT',
    author="Nguyen Tien Nam",
    author_email='a@example.com',
    packages=find_packages('solvers'),
    package_dir={'': 'solvers'},
    keywords='linear solvers',
    install_requires=[
          'numpy',
      ],

)