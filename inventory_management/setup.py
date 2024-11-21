from setuptools import setup, find_packages

setup(
    name="inventory_management",
    version="0.1.0",
    author="kevin mai",
    author_email="shihao.mai@outlook.com",
    description="inventory management system",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/maikevin1/inventory_management",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        # if need
    ],
)
