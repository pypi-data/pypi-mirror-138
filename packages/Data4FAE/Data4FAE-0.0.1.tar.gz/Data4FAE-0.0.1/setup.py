from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


VERSION = '0.0.1'
DESCRIPTION = 'Python package for Satellogic interview'
LONG_DESCRIPTION = 'generating some data from remote database'

# Setting up
setup(
    # the name must match the folder name '2Data4FAE'
    name="Data4FAE",
    version=VERSION,
    author="Gabriel Rosso",
    author_email="<rosso.gabriel1@gmail.com>",
    description=DESCRIPTION,
    long_description=readme(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['pandas', 'matplotlib', 'seaborn', 'folium', 'dms2dec',],  # add any additional packages

    keywords=['python', 'first package'],
        classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"),
)
