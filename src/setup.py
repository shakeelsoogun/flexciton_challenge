from setuptools import setup

setup(
    name="scheduler",
    version="1.0",
    py_modules=["main"],
    include_package_data=True,
    install_requires=["click"],
    entry_points="""
        [console_scripts]
        scheduler=main:main
    """,
)