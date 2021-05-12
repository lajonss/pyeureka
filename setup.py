from distutils.core import setup
setup(
    name="pyeureka",
    version="2021.5.12.0",
    author="Paweł Białas",
    author_email="gfs.b16@gmail.com",
    url="https://github.com/lajonss/pyeureka",
    description="Netflix Eureka REST API access library",
    packages=["pyeureka"],
    install_requires=['requests'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries"
    ]
)
