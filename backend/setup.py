from setuptools import setup, find_packages
import os


def read_requirements():
    with open("requirements.txt") as requirements_file:
        return [
            line.strip()
            for line in requirements_file
            if line.strip() and not line.startswith("#")
        ]


setup(
    name="resoursphere-backend",
    version="0.0.5",
    packages=find_packages(),
    package_dir={"": "."},
    install_requires=read_requirements(),
    include_package_data=True,
    package_data={
        "app": ["config/*.yml"],
        "app.endpoints": ["*/*.py"],
    },
    entry_points={
        "console_scripts": [
            "resoursphere-backend=app.main:run_app",
        ],
    },
    author="Roy Sahar",
    description="Backend service for managing AWS resources with role-based access control",
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: DevOps teams and developeres",
        # "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
) 