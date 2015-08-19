from setuptools import setup, find_packages

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='schematics',
      version='0.1',
      description='Create schematics of thermal-hydraulic systems',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Text Processing :: Linguistic',
      ],
      keywords='schematics thermal hydraulic graph',
      url=None,
      author='Andrew Franklin',
      author_email='andrew.franklin@inl.gov',
      license='MIT',
      packages=find_packages(),
      # install_requires=[
      #     'matplotlib',
      # ],
      test_suite='nose.collector',
      tests_require=['nose'],
      # scripts=['bin/funniest-joke'],
      zip_safe=False)
