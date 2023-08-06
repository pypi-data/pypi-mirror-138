from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(name='calcalc-toy',
      version='1.7',
      description='A calculator that evaluates string expressions ' +
                  'both locally or using WolframAlpha.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Yang Lyu',
      author_email='yanglyu902@gmail.com',
      python_requires='>=3',
      license='MIT License',
      packages=['calcalc'],
      )
