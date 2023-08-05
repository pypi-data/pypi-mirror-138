from setuptools import setup

setup(
    name="dewr",
    version="0.0.7",
    description="A small example package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="churunmin",
    author_email="churunmin@outlook.com",
    url="https://github.com/pypa/sampleproject",
    license="MIT",
    packages=["dewr"],
    entry_points={
        "console_scripts": ["dewr=dewr.cli:main"],
    },
    install_requires=[
        'pywin32; sys_platform == "win32"',
        'pyobjc; sys_platform == "darwin"',
    ],
    python_requires=">=3.6",
)
