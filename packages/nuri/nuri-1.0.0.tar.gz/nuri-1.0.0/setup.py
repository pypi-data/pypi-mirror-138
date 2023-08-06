import pathlib
import pkg_resources
from setuptools import setup,find_packages
from glob import glob
import nuri

with pathlib.Path('requirements.txt').open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]

with open('README.md', 'r') as f:
    longdesc = f.read()

setup(
    name="nuri",
    version=nuri.__version__,
    description="Time-frequency and sensor network analysis software for urban magnetometry data.",
    long_description=longdesc,
    long_description_content_type='text/markdown',
    scripts = glob('bin/*'),
    author="Vincent Dumont",
    author_email="vincentdumont11@gmail.com",
    maintainer="Vincent Dumont",
    maintainer_email="vincentdumont11@gmail.com",
    url="http://citymag.gitlab.io/nuri/",
    license_files = ('LICENSE.txt',),
    packages=find_packages(include=('nuri*',)),
    project_urls={
        "Source Code": "https://gitlab.com/citymag/analysis/nuri",
    },
    install_requires=["astropy","gwpy","h5py","matplotlib","numpy"],
    classifiers=[
        'Intended Audience :: Science/Research',
        "License :: Other/Proprietary License",
        'Natural Language :: English',
        "Operating System :: OS Independent",
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Physics',
    ],

)
