from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Ml tracking tool using jupyter extensions'
LONG_DESCRIPTION = 'A package that allows users to track their ML experiments within jupyter notebook.'

# Setting up
setup(
    name="MlTrackTool",
    version=VERSION,
    author="Anesh",
    url="https://github.com/anesh-ml/ML_tracking_tool",
    author_email="analytics955@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    py_modules=["edit_sheet","Explainer","metrics","OpenSheet","utils"],
    install_requires=['ipysheet', 'scikit-plot', 'lime','Shapely'],
    keywords=['python', 'Machine learning', 'MLops', 'ML tracking system'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)