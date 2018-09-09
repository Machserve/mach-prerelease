# -*- coding: utf-8 -*-

import codecs
import os
import re

from setuptools import find_packages, setup


here = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
	with codecs.open(os.path.join(here, *parts), 'r') as fp:
		return fp.read()


def find_version(*file_paths):
	version_file = read(*file_paths)
	version_match = re.search(
		r"^__version__ = ['\"]([^'\"]*)['\"]", 
		version_file, 
		re.M
	)
	if version_match:
		return version_match.group(1)
	raise RuntimeError("Unable to find version string.")


setup(
	name="mach_prerelease",
	version=find_version("mach_prerelease", "__init__.py"),
	description="Prerelease landing portal for machserve.io",
	packages=find_packages(),
	include_package_data=True,
	install_requires=["aiohttp", "aiohttp_jinja2"],
	zip_safe=False,
)