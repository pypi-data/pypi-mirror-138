import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="servyou-log",
    version="1.4",
    author="PubDesktopLsw",
    description='日志工具类',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    platforms=["all"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>2',
    install_requires=[
        'concurrent-log-handler == 0.9.11',
    ]
)
