# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open(r"requirements.txt", "r") as f:
    reqs = f.read()

reqs = reqs.replace(" ", "")
reqs = reqs.split("\n")
reqs = [x for x in reqs if "#" not in x ]
reqs = [x for x in reqs if "pyhdf" not in x]
reqs = ' '.join(reqs)
reqs = reqs.split()

setup(
    name='TOLNet',
    version="2024.06.18",
    author='Maurice Roots',
    author_email='themauriceroots@gmail.com',
    description='Tropospheric Ozone Lidar Network (TOLNet) API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/moroots/TOLNET_Summer',
    project_urls = {
        "Bug Tracker": "https://github.com/moroots/TOLNEt_Summer/issues"
    },
    license='MIT',
    packages=find_packages(),
    install_requires=reqs,
)