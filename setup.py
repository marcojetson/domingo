from setuptools import setup

setup(
    name="domingo",
    version="0.1.0",
    packages=["domingo", "domingo.commands", "domingo.normalizations"],
    entry_points={
        "console_scripts": [
            "domingo=domingo.__main__"
        ]
    }
)
