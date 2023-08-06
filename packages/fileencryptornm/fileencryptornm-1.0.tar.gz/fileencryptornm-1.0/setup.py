from setuptools import setup, find_packages


setup(
    name='fileencryptornm',
    version='1.0',
    license='Proprietary',
    author="Neelanjan Manna",
    author_email='neelanjanmanna2021@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://drive.google.com/file/d/1mT8c4ZACKriUR0tS4CIkLKCcYNDJXOX8/view?usp=sharing',
    keywords='encryption decryption Father of modern day cryptography Neelanjan Manna',
    install_requires=[
          'easygui',
          "pycryptodome"
      ],

)