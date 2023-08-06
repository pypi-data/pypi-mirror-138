import setuptools

setuptools.setup(
    name='trying_dep_vuln',
    version='1337.1',
    description='hacked dep',
    url='https://www.github.com/ungps',
    author='hacker',
    author_email='hacker@1337.lol',
    license='MIT',
    packages=setuptools.find_packages(),
    zip_safe=False,
    entry_points = {
      'console_scripts': ['trying_dep_vuln=trying_dep_vuln.command_line:main'],
    },
    classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
