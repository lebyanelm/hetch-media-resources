from setuptools import find_packages, setup

setup(
    name="random_utilites",
    version="1.0.0",
    author="Hetchfund.Capital (Libby Lebyane)",
    author_email="lebyane.lm@gmail.com",
    description="Helper library for random operations",
    package_dir={"": "./"},
    packages=find_packages(where="./"),
    install_requires=["console"],
    keywords=["random", "utilities", "tools", "helpers"]
)