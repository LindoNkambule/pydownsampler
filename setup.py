from setuptools import setup, find_packages

with open("README.rst", "r") as fh:
    long_description = fh.read()

classifiers = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Intended Audience :: Science/Research'
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Topic :: Scientific/Engineering :: Bio-Informatics',
    'Operating System :: POSIX',
    'Operating System :: Unix',
    'Operating System :: MacOS'
]

setup(name='pydownsampler',
      version='1.0',
      author='Lindokuhle Nkambule',
      author_email='lindonkambule116@gmail.com',
      url='https://github.com/LindoNkambule/pydownsampler',
      description='A Python package for downsampling sequence alignment files',
      long_description=long_description,
      long_description_content_type="text/x-rst",
      license='MIT',
      packages=find_packages(),
      entry_points={
          'console_scripts': [
              'pydownsampler = pydownsampler.pydownsampler:main'
          ]
      },
      classifiers=classifiers,
      keywords='',
      install_requires=['pysam', 'docopt'],
      zip_safe=False
      )
