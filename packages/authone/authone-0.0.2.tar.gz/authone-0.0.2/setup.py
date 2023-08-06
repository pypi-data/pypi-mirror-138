from os.path import join
from os.path import dirname

from setuptools import find_packages
from setuptools import setup


def read_version():
    version_contents = {}
    with open(join(dirname(__file__), 'authone', 'version.py')) as fh:
        exec(fh.read(), version_contents)

    return version_contents['VERSION']

def load_readme():
    return "AuthOne Python Library"


INSTALL_REQUIRES = [
    "requests >= 2.22.0, <3",
    "web3 >= 4.8.1, <6"
]


setup(
    name='authone',
    version=read_version(),
    description='AuthOne Python Library',
    long_description=load_readme(),
    long_description_content_type='text/markdown',
    author='AuthOne',
    author_email='AuthOne@housechan.com',
    url='https://github.com/Generative-Labs/AuthOne-Python',
    license='MIT',
    keywords='AuthOne python sdk',
    packages=find_packages(
        exclude=[
            'tests',
            'tests.*',
            'testing',
            'testing.*',
            'virtualenv_run',
            'virtualenv_run.*',
        ],
    ),
    zip_safe=False,
    install_requires=INSTALL_REQUIRES,
    python_requires='>=3.6',
    project_urls={
        'Website': 'https://github.com/Generative-Labs/AuthOne-Python',
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
