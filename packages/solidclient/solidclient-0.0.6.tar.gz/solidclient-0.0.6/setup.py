from setuptools import setup, find_packages

setup(name='solidclient',
      version='0.0.6',
      description='A Solid client in Python',
      url='https://gitlab.com/arbetsformedlingen/individdata/oak/python-solid-client',
      author='Max Dzyuba',
      author_email='max.dzyuba@arbetsformedlingen.se',
      license='MIT',
      packages=find_packages(exclude=["tests"]),
      install_requires=[
          'requests',
          'jwcrypto',
          'rdflib',
          'solid-file',
          'oic',
          'httpx==0.18.2',
      ],
      python_requires='>= 3.6',
      )
