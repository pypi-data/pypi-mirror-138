import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

requirements: list = ["setuptools", "requests", "nest_asyncio", "six>=1.9.0", "websocket-client>=0.54.0",
                      "websockets>=7.0", "aiohttp>=3.4", "bidict"]

setuptools.setup(
    name='nertivia',  # How you named your package folder (MyLib)
    version='0.3.0',  # Start with a small number and increase it with every change you make
    license='apache-2.0',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='Deprecated version of nertivia for python',  # Give a short description about
    # your library
    long_description= long_description,
    long_description_content_type="text/markdown",
    keywords=['API Wrapper', 'SIMPLE', 'PYTHON'],  # Keywords that define your package best
    packages=setuptools.find_namespace_packages(include=['nertivia']),
    python_requires=">=3.6",
    classifiers=[
        'Development Status :: 7 - Inactive',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Programming Language :: Python :: 3',  # Specify which python versions that you want to support
    ],
)