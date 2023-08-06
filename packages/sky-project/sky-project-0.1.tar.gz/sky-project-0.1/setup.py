from setuptools import setup, find_packages


setup(
    name='sky-project',
    version='0.1',
    author="Zongheng Yang",
    author_email='zongheng.y@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/gmyrianthous/example-publish-pypi',
    keywords='example project',
    install_requires=[
          'scikit-learn',
      ],
)
