from setuptools import setup


setup(
    install_requires=[
        "grpcio",
        "protobuf"
    ],
    test_suite="tests",
    tests_require=["pytest"],
)
