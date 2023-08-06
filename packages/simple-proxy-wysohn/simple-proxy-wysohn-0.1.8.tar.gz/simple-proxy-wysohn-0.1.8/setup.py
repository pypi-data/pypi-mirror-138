import setuptools

setuptools.setup(
    name='simple-proxy-wysohn',
    version='0.1.8',
    author='wysohn',
    author_email='wysohn2002@naver.com',
    python_requires='>=3.6',
    packages=setuptools.find_packages(),
    install_requires=[
        'requests',
        'bs4',
        'selenium',
        'html5lib',
        'pysocks',
    ],
)
