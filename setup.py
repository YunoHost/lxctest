from setuptools import setup

setup(name='lxctest',
      version='0.1',
      description='Provides a wrapper around LXC to automate test execution',
      author='Joshua Powers',
      author_email='josh.powers@canonical.com',
      url='http://github.com/powersj/lxctest',
      keywords=['lxc', 'test'],
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Environment :: Console",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: GNU General Public License v3 or later"
          " (GPLv3+)",
          "Natural Language :: English",
          "Operating System :: POSIX :: Linux",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3.5",
          "Topic :: Software Development :: Quality Assurance",
          "Topic :: Software Development :: Testing",
      ],
      packages=['lxctest'],
      zip_safe=False)
