import setuptools

REQUIRES = [
    'aiohttp>=3.5.4',
]

with open("README.rst") as fh:
    long_description = fh.read()

setuptools.setup(
    name='xcomfortshc',
    version='0.1',
    description= 'Eaton xComfort Smart Home Controller communinication library.',
    long_description=long_description,
    url='https://github.com/plamish/xcomfort-shc',
    license='MIT',
    packages=['xcomfortshc'],
    install_requires=REQUIRES,
    python_requires='>=3.6.0',
    author='plamish',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
