from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]


setup(
    name='NoelNLP',
    version = '0.0.2',
    description = 'Swahili Stop-words and Stemmer',
    long_description=open('README.txt').read(),
    url = '',
    author = 'Noel Moses Mwadende',
    author_email='mosesnoel02@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='Swahili Stop-words,NLTK,NLP',
    packages=find_packages(),
    install_requires = []
)
