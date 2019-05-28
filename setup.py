from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='annotater',
      version='0.1',
      description='The python program to annotate a VCF',
      long_description=readme(),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python :: 3.6',
      ],
      url='https://github.com/BrettKennedy/annotater',
      author='Brett Kennedy',
      author_email='brett.jacob.kennedy@gmail.com',
      packages=find_packages(),
      install_requires=[
          'pysam'
      ],
      package_data={'annotater': [
          'data/*.vcf', 'data/*.csv']},
      entry_points={
          'console_scripts': ['annotater=annotater.__main__:main'],
      },
      include_package_data=True,
      zip_safe=False)
