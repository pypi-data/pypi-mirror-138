import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="screenmonkey",
    version="0.1.0",
    author="brycemerrill",
    author_email="brycelmerrill@gmail.com",
    description="Packing for recording and executing on-screen actions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bmerrill17/screenmonkey",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    install_requires=['pandas', 'openpyxl', 'pynput'],
    python_requires=">=3.6",
)