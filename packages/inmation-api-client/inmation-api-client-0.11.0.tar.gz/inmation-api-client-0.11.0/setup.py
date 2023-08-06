import sys
import setuptools

py_version = sys.version_info[:2]

if py_version < (3, 7):
    raise Exception("websockets requires Python >= 3.7.")

with open("README.md", "r") as fh:
    long_description = fh.read()

exec(open("inmation_api_client/_version.py").read())

setuptools.setup(
    name="inmation-api-client",
    version=__version__,
    author="inmation Software GmbH",
    author_email="support@inmation.com",
    license='MIT',
    description="API client for system:inmation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://inmation.com",
    packages=setuptools.find_packages(),
    install_requires=[
        'websockets==10.1',
    ],
    classifiers=(
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ),
    zip_safe=True,
    python_requires='>=3.7, <3.11',
)
