from setuptools import setup, find_packages

setup(
      description = 'A package to determine the best Wordle guesses.',
      name = 'WordleGuesser',
      author = 'Patrick McCullough',
      version = '0.1.0',
      classifiers = [
          'Programming Language :: Python :: 3',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent'],
      packages = find_packages(),
      python_requires = '>=3')

