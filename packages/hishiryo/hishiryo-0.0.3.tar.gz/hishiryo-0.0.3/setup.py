import setuptools
from glob import glob

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hishiryo", 
    version="0.0.3",
    author="Nicolas Boisseau",
    author_email="spriggancg@gmail.com",
    description="Render a dataset into a picture",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/spriggancg/hishiryo",
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    install_requires=['pandas<=1.3.5', 'opencv-python'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Topic :: Artistic Software",
        "Operating System :: MacOS :: MacOS X",
    ],
    python_requires='>=3.6',
)
