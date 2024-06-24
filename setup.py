from setuptools import setup, find_packages

setup(
    name="fastapi-cacher",
    version="0.1.0",
    author="Fahad Mawlood",
    author_email="fahadukr@gmail.com",
    description="A caching library for FastAPI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Fahadukr/fastapi-cacher",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "redis",  # or any other dependencies
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
