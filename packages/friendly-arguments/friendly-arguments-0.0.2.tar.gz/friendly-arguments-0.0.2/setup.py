from setuptools import find_packages, setup

with open('README.md', 'rb') as f:
    readme = f.read().decode('utf-8')

setup(
    name='friendly-arguments',
    packages=find_packages(),
    version='0.0.2',
    description='Easy way to use named arguments by means of python dictionaries',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='Meu Nome',
    author_email='meu@email.com',
    url='https://github.com/usuario/meu-pacote-python',
    install_requires=[],
    license='MIT',
    keywords=['dev', 'scripts', 'args', 'tools'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
)