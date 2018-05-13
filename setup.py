from setuptools import setup

setup(name='game_theory_toolkit',
      version='0.1',
      description='Game Theory Tools',
      long_description='tools for game theory analysis and simulations',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Game Theory :: Mechanism Design',
      ],
      keywords='game theory mechanism design',
      url='http://github.com/storborg/funniest',
      author='Youcef Msaid',
      author_email='youcef.msaid@gmail.com',
      license='MIT',
      packages=['game_theory_toolkit'],
      install_requires=[
          'numpy',
          'random',
          'itertools',
      ],
      include_package_data=True,
      zip_safe=False)