from setuptools import setup, find_packages

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(name='pydownsampler',
      version='1.0',
      author='Lindokuhle Nkambule',
      author_email='lindonkambule116@gmail.com',
      url='https://github.com/LindoNkambule/pydownsampler',
      description='A Python package for downsampling BAM files',
      long_description=long_description,
      long_description_content_type="text/x-rst",
      license='MIT',
      packages=find_packages(),
      entry_points={
          'console_scripts': [
              'pydownsampler = pydownsampler.pydownsampler:main'
          ]
      },
      classifiers=(
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ),
      keywords='',
      install_requires=['pysam', 'docopt'],
      zip_safe=False
      )
