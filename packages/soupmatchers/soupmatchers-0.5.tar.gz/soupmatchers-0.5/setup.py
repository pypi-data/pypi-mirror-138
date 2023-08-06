from setuptools import setup


# generic helpers primarily for the long_description
def generate(*docname_or_string):
    marker = '.. pypi description ends here'
    res = []
    for value in docname_or_string:
        if value.endswith('.rst'):
            with open(value) as f:
                value = f.read()
            idx = value.find(marker)
            if idx >= 0:
                value = value[:idx]
        res.append(value)
        if not value.endswith('\n'):
            res.append('')
    return '\n'.join(res)
# end generic helpers


setup(
    name='soupmatchers',
    version='0.5',
    description='Matchers for checking parts of a HTML parse tree',
    url='http://launchpad.net/soupmatchers',
    license='Eclipse Public License',
    packages=['soupmatchers',],
    long_description=generate('README.rst'),
    setup_requires=['setuptools'],
    install_requires=['testtools>0.9.3', 'beautifulsoup4'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Eclipse Public License 1.0 (EPL-1.0)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Text Processing :: Markup :: HTML",
        "Topic :: Software Development :: Testing",
        ],
    )
