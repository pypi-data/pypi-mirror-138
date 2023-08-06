# References
# https://packaging.python.org/tutorials/packaging-projects/
# https://www.geeksforgeeks.org/how-to-publish-python-package-at-pypi-using-twine-module/
# https://stackoverflow.com/questions/45168408/creating-tar-gz-in-dist-folder-with-python-setup-py-install
# https://docs.python.org/3/distutils/sourcedist.html
# https://github.com/conda-incubator/grayskull


import setuptools


def _make_long_description():
	with open("README.md", "r", encoding="utf-8") as readme_file:
		long_description = readme_file.read()

	start_index = long_description.index("## Français")

	return long_description[start_index:]


def _make_requirement_list():
	with open("requirements.txt", "r", encoding="utf-8") as req_file:
		req_str = req_file.read()

	requirements = req_str.split("\n")

	i = 0
	while i < len(requirements):
		if len(requirements[i]) == 0:
			del requirements[i]
		i += 1

	return requirements


setuptools.setup(
	name = "PyPDF2_Fields",
	version = "0.1.0",
	author = "Guyllaume Rousseau",
	description = "Library PyPDF2_Fields is a complement to PyPDF2. It helps using a PDF file’s fields by facilitating several tasks.",
	long_description = _make_long_description(),
	long_description_content_type = "text/markdown",
	url = "https://github.com/GRV96/PyPDF2_Fields",
	classifiers = [
		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
		"Programming Language :: Python :: 3",
		"Topic :: Software Development :: Libraries :: Python Modules",
		"Topic :: Utilities"
	],
	install_requires = _make_requirement_list(),
	packages = setuptools.find_packages(exclude=("tests",)),
	license = "MIT",
	license_files = ("LICENSE",)
)
