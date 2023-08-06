import io
from setuptools import setup, find_packages
from swis.swis import __version__


def get_requirements():
    with open('requirements.txt') as fp:
        return [req for req in (line.strip() for line in fp) if req and not req.startswith('#')]


setup(
    name='swis',
    version=__version__,
    author='Robert Susik',
    author_email='robert.susik@gmail.com',
    options={'bdist_wheel': {'universal': True}},    
    license='GPLv3',
    description=(
        '''Simple Web-based Interface for Scanner written in Python and JavaScript.'''
    ),
    long_description=io.open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'swis=swis.swis:main',
        ],
    },
    package_data={'': ['app/*', 'app/*/*', 'app/*/*/*', 'app/*/*/*/*', 'app/*/*/*/*/*', 'app/*/*/*/*/*/*', 'assets/*']},
    install_requires=get_requirements(),
    package_dir={'': '.'},
    packages=find_packages(where='.'),
    url='https://github.com/rsusik/simple-web-based-interface-for-scanner',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: JavaScript',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        'Operating System :: POSIX :: Linux',
        'Framework :: FastAPI',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Printing',
        'Topic :: Multimedia :: Graphics :: Capture :: Scanners',
        'Topic :: Utilities',
    ],
)
