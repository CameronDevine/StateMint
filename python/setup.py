import setuptools

with open('README.md') as f:
	long_description=f.read()

setuptools.setup(
	name="StateMint",
	version="2.1.0",
	author="Cameron Devine",
	author_email="camdev@uw.edu",
	description="A library for finding State Space models of dynamical systems.",
	long_description=long_description,
	long_description_content_type='text/markdown',
	url="https://github.com/CameronDevine/StateMint",
	packages=setuptools.find_packages(),
	python_requires=">=2.7",
	install_requires=("sympy>=0.7.3",),
	classifiers=(
		"Development Status :: 4 - Beta",
		"Framework :: Jupyter",
		"Intended Audience :: Education",
		"Intended Audience :: Science/Research",
		"License :: OSI Approved :: BSD License",
		"Programming Language :: Python :: 2",
		"Programming Language :: Python :: 2.7",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.0",
		"Programming Language :: Python :: 3.1",
		"Programming Language :: Python :: 3.2",
		"Programming Language :: Python :: 3.3",
		"Programming Language :: Python :: 3.4",
		"Programming Language :: Python :: 3.5",
		"Programming Language :: Python :: 3.6",
		"Operating System :: OS Independent",
	),
)
