from setuptools import setup, find_packages

setup(
    name='simptoolbox',
    version='0.1.2',
    description='Simple Class Manager',
    url='https://github.com/StephenMal/simptoolbox',
    author='Stephen Maldonado',
    author_email='simptoolbox@stephenmal.com',
    packages=find_packages(),
    install_requires=['simplogger'],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Utilities'
    ]
)
