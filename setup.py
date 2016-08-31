from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='lxctest',
      version='1.0.11',
      description='Provides a wrapper around LXC via the lxd-client tools to '
                  'automate test execution',
      long_description=readme(),
      author='Joshua Powers',
      author_email='josh.powers@canonical.com',
      url='https://github.com/powersj/lxctest',
      download_url='https://github.com/powersj/lxctest/tarball/master',
      keywords=['lxc', 'test'],
      license='GNU General Public License v3 or later',
      classifiers=[
          "Development Status :: 4 - Beta",
          "Environment :: Console",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: GNU General Public License v3 or later"
          " (GPLv3+)",
          "Natural Language :: English",
          "Operating System :: POSIX :: Linux",
          "Programming Language :: Python :: 3 :: Only",
          "Programming Language :: Python :: 3.5",
          "Topic :: Software Development :: Quality Assurance",
          "Topic :: Software Development :: Testing",
      ],
      packages=['lxctest'],
      entry_points={
          'console_scripts': ['lxctest=lxctest.lxctest:init']
      },
      install_requires=['PyYAML'],
      zip_safe=False
      )
