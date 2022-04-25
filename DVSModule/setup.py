from setuptools import setup

setup(
    name='DVSModule',
    version='1.0.0',    
    description='A example Python package',
    url='https://gitlab.univ-lille.fr/clement.saulquin.etu/dvsevents',
    author='Saulquin Clément',
    author_email='clement.saulquin.etu@univ.lille.fr',
    packages=['DVSModule'],
    install_requires=['nengo',
                      'numpy',                     
                      ],

    classifiers=[
        'Development Status :: Fonctionnal',
        'Intended Audience :: Science/Research',
        'Operating System :: POSIX :: Linux',       
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)