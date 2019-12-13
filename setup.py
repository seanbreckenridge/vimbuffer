import io
from setuptools import setup, find_packages

requirements = []

# Use the README.md content for the long description:
with io.open('README.md', encoding='utf-8') as fo:
    long_description = fo.read()

setup(
    name='vimbuffer',
    version="0.1.0",
    url='https://github.com/seanbreckenridge/vimbuffer',
    author='Sean Breckenridge',
    author_email='seanbrecke@gmail.com',
    description="Edit files, and strings in temporary vim (or some other console editor) buffers.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    packages=find_packages(include=['vimbuffer']),
    test_suite='tests',
    install_requires=requirements,
    keywords='vim editor stream',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
)