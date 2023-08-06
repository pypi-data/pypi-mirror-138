import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "aws-cdk-microservice",
    "version": "0.0.15",
    "description": "@smallcase/aws-cdk-microservice",
    "license": "Apache-2.0",
    "url": "https://github.com/smallcase/aws-cdk-microservice.git",
    "long_description_content_type": "text/markdown",
    "author": "Gagan Singh<gaganpreet.singh@smallcase.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/smallcase/aws-cdk-microservice.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "aws_cdk_microservice",
        "aws_cdk_microservice._jsii"
    ],
    "package_data": {
        "aws_cdk_microservice._jsii": [
            "aws-cdk-microservice@0.0.15.jsii.tgz"
        ],
        "aws_cdk_microservice": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk-lib==2.8.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.54.0, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
