from setuptools import setup
setup(
        name='pyt',
        version='1.0.0',
        description='Twitter Client',
        long_description='',
        url='example.com',
        author='me',
        author_email='me@lol.com',
        license='MIT',

        classifiers=[
            'Programming Language :: Python :: 3'
            'License :: OSI Approved :: MIT License',
            ],
        install_requires=['requests', 'tweepy', 'bottle'],
        packages=['gui', 'common', 'server'],
        entry_points={
            'console_scripts': [
                'pyt=gui:main',
                'servpyt=server:main',
                ],
            },
)
