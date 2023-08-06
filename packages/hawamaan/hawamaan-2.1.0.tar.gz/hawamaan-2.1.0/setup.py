from setuptools import setup
setup(
  name = 'hawamaan',         #* Your package will have this name
  packages = ['hawamaan'],   #* Name the package again
  version = '2.1.0',         #* To be increased every time your change your library
  license='MIT',             # Type of license. More here: https://help.github.com/articles/licensing-a-repository
  description = 'Weather forecast data',    # Short description of your library
  author = 'Sagar Pitalekar',                   # Your name
  author_email = 'pypi.cloudfoundry276@gmail.com',  # Your email
  url = 'https://github.com/CloudFoundry276/WeatherForecastLibrary',              # Homepage of your library (e.g. github or your website)
  keywords = ['weather', 'forecast', 'openweather'],   # Keywords users can search on pypi.org
  install_requires=[
    'requests',
    ],
  classifiers=[
    'Development Status :: 3 - Alpha',          # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',          # Who is the audience for your library?
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Type a license again
    'Programming Language :: Python :: 3.5',      # Python versions that your library supports
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)