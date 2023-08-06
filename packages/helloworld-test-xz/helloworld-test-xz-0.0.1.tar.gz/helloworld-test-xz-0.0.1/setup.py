from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
        name="helloworld-test-xz",
        version="0.0.1",
        description="say hello",
        long_description=long_description,
        long_description_content_type="text/markdown",
        py_modules=["helloworld"],
        url='https://github.com/zxx2643/helloworld',
        author='Xiaoxuan Zhang',
        author_email='zhangxiaoxuan258@gmail.com',
        package_dir={"":"src"},
        classifiers=[
            "Programming Language :: Python :: 3.6",
            "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
            ],
        install_requires=[
          'numpy',
          ],
        extras_require = {
            "dev":[
                "pytest>=3.7",
                ],
            },
        )
