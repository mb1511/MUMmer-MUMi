import sys
from setuptools import setup

path_to_mummer = sys.argv.pop()
t = []
with open('mumi/__init__.py') as r:
    m_set = False
    for line in r:
        if not m_set:
            if line.startswith('mummer'):
                line = "mummer = '%s'\n" % path_to_mummer
                m_set = True
        t.append(line)
with open('mumi/__init__.py', 'w') as w:
    w.write(''.join(t))

def readme():
    with open('README.md') as s:
        return s.read()

setup(
    name='mumi',
    version='0.1',
    description='MUMi Python API',
    long_description=readme(),
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
    ],
    url='https://github.com/mb1511/MUMmer-MUMi',
    author='Matt Brewer',
    author_email='mb1511@bristol.ac.uk',
    license='GPLv3',
    packages=['mumi'],
    install_requires=['dill', 'numpy'],
    zip_safe=False)

