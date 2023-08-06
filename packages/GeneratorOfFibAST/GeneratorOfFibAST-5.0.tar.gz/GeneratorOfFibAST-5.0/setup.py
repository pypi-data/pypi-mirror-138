import setuptools

install_requires = ["graphviz==0.19.1",
                    "pygraphviz==1.8"]

setuptools.setup(
    name="GeneratorOfFibAST",
    version="5.0",
    author="Braun Kate",
    install_requires=install_requires,
    url="https://github.com/Frosendroska/AdvancedPython-2022",
    package_dir={"": "src/GeneratorOfFibAST"},
    packages=setuptools.find_packages(where="src/GeneratorOfFibAST"),
    python_requires=">=3.9",
)
