from distutils.core import setup

setup(
    name='q3api',  # How you named your package folder (MyLib)
    packages=['q3api'],  # Chose the same as "name"
    version='0.1',  # Start with a small number and increase it with every change you make
    license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='simple minimalistic API for quake 3 (arena) server status',  # Give a short description about your library
    author='Boris Khesin',  # Type in your name
    author_email='rob.falls.do@gmail.com',  # Type in your E-Mail
    url='https://github.com/Shagulka/q3-api',  # Provide either the link to your github or to your website
    download_url='https://github.com/Shagulka/q3-api/archive/refs/tags/v0.1.tar.gz',  # I explain this later on
    keywords=['QUAKE3', 'API'],  # Keywords that define your package best
    install_requires=[],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3',  # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
