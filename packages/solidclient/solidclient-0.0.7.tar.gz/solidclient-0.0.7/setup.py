from setuptools import setup, find_packages

setup(name='solidclient',
      version='0.0.7',
      description='A Solid client in Python',
      url='https://gitlab.com/arbetsformedlingen/individdata/oak/python-solid-client',
      author='Max Dzyuba',
      author_email='max.dzyuba@arbetsformedlingen.se',
      license='MIT',
      keywords='Solid Client OpenID Connect OIDC DPoP',
      packages=find_packages(exclude=["tests"]),
      install_requires=[
          'requests==2.25.1',
          'jwcrypto==1.0',
          'rdflib==5.0.0',
          'solid-file==0.2.0',
          'oic==1.3.0',
          'httpx==0.18.2',
      ],
      python_requires='>= 3.6',
      test_suite='tests',
      )
