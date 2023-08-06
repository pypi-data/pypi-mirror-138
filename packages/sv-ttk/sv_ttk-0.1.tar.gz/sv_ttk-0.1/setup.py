from setuptools import setup

setup(
    name="sv_ttk",
    version=0.1,
    description="Python module to easily use the Sun Valley ttk theme",
    author="rdbende",
    author_email="rdbende@gmail.com",
    url="https://github.com/rdbende/Sun-Valley-ttk-theme",
    python_requires=">=3.4",
    license="MIT license",
    classifiers=[
        "Programming Language :: Python :: 3.4",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["sv_ttk"],
    package_data={
        "sv_ttk": ["sun-valley.tcl", "theme/*", "theme/dark/*", "theme/light/*"]
    },
)
