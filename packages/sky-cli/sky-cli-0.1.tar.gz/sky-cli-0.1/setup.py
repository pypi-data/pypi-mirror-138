from setuptools import setup, find_packages


setup(
    name='sky-cli',
    version='0.1',
    license='MIT',
    author="Sky Team",
    author_email='email@example.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/',
    keywords='Sky CLI',
    install_requires=[
          'ray',
      ],

)
