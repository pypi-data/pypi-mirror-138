from setuptools import setup

setup(
    name='graypy_gelf_https',
    version='1.0.1',
    description='graypy extension with GELF HTTPS handler',
    license='MIT',
    author='Dmitrii Don',
    author_email='dondmitriys@gmail.com',
    packages=['graypy_gelf_https', ],
    url='https://github.com/smpio/graypy-gelf-https',
    keywords='logging gelf graylog https',
    install_requires=[
        'graypy<2.2.0',
        'urllib3<1.27.0',
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.9',
        'Topic :: System :: Logging',
    ],
)
