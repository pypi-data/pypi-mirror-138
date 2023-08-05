from setuptools import setup, find_packages

VERSION='0,1'

setup(
    name="librarios",
    version=VERSION,
    description="A Library Management Program on python And MySQL",
    author="Anshuman",
    author_email="<anshumankhatri2004@gmail.com>",
    url="https://github.com/AnshumanKhatri14/Librarios",
    install_requires=['mysql.connector','datetime'],
    keywords=['python','mysql'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)











