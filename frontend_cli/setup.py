from setuptools import setup, find_packages


def read_requirements():
    with open("requirements.txt") as requirements_file:
        return [
            line.strip()
            for line in requirements_file
            if line.strip() and not line.startswith("#")
        ]


setup(
    name="resoursphere",
    version="0.1.0",
    packages=find_packages(),
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "resoursphere=app.main:resoursphere_client",
        ],
    },
    author="Roy Sahar",
    description="CLI tool to manage AWS resources",
    python_requires=">=3.7",
)
