from setuptools import setup, find_packages


setup(name='calcalc-toy',
      version='1.5',
      description='A calculator that evaluates string expressions ' +
                  'both locally or using WolframAlpha.',
      long_description='A calculator that evaluates string numerical expressions ' +
                       'both locally or using WolframAlpha.',
      long_description_content_type="text/markdown",
      author='Yang Lyu',
      author_email='yanglyu902@gmail.com',
      python_requires='>=3',
      license='MIT License',
      packages=['calcalc'],
    )
