from setuptools import setup, find_packages

setup(
    name="binho",
    author="Clint Lawrence",
    author_email="clint.lawrence@gmail.com",
    package_dir={'': 'src'},
    packages=find_packages('src'),
    version="0.0.1",
    install_requires=[
        'pyserial',
    ],
    # entry_points="""
    #     [console_scripts]
    #     binho=binho.cli:main
    #     """,
)