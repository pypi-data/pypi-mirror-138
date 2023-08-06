import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
with open('CHANGELOG.md', 'r') as f:
    changelog = f.read()

setuptools.setup(
    name="xcsr",
    version="1.0.0",
    author="xKyFal",
    description="A simple comic scraper.",
    long_description="{}\n\n{}".format(long_description, changelog),
    long_description_content_type="text/markdown",
    url="https://github.com/nordic16/xcsr-git",
    project_urls={
        "Bug Tracker": "https://github.com/nordic16/xcsr-git/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        'Intended Audience :: End Users/Desktop',
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    keywords='command-line, cli, comics, scraper',
    packages=setuptools.find_namespace_packages(include=('src.xcsr')),
    python_requires=">=3.6",
    
    entry_points="""
    [console_scripts]
    xcsr=xcsr.xcsr:main
    """,
)
