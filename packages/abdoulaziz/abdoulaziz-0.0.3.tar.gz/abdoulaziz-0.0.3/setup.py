from distutils.core import setup
setup(
  name = 'abdoulaziz',         # How you named your package folder (MyLib)
  packages = ['abdoulaziz'],   # Chose the same as "name"
  version = '0.0.3',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'TYPE YOUR DESCRIPTION HERE',   # Give a short description about your library
  author = 'Abdoul Aziz Berrada',                   # Type in your name
  author_email = 'abdoulazizberrada@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/aadmberrada/abdoulaziz',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/aadmberrada/abdoulaziz/archive/v_003.tar.gz',    # I explain this later on
  package_dir={'': '/Users/abdoul_aziz_berrada/Documents/Data Science'},
  keywords = ['SOME', 'MEANINGFULL', 'KEYWORDS'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'validators'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)