
from distutils.core import setup
setup(
  name = 'C5_common_libraries',                 # How you named your package folder (MyLib)
  packages = ['C5_common_libraries'],           # Chose the same as "name"
  version = '0.8',                              # Start with a small number and increase it with every change you make
  license='MIT',                                # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'This library is for C5 team, here we have created some common functions that we use while coding. Note : this library is completely useless for the outside world',   # Give a short description about your library
  author = 'Prathamesh Patil',                  # Type in your name
  author_email = 'prathamesh.patil@course5i.com',      # Type in your E-Mail
  url = 'https://github.com/pprathamesh7',      # Provide either the link to your github or to your website
  download_url = 'https://github.com/pprathamesh7/C5_common_libraries/archive/refs/tags/v_01.0.5.tar.gz',    # I explain this later on
  keywords = ['C5', 'Course5', 'Course5i'],     # Keywords that define your package best
  install_requires=[                            # I get to this in a second
          'pandas',
          'pathlib'],
  classifiers=[
    'Development Status :: 4 - Beta',           # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',           # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',    # Again, pick a license  
    'Programming Language :: Python :: 3.7',     #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)
