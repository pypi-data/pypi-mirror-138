from setuptools import setup
#python -m twine upload dist/* --repository-url https://test.pypi.org/legacy/
setup(
    name = 'matpack',
    version = '1.0.5',
    author = 'Thiarly Souza',
    author_email = 'Thiarly@ufrn.edu.br',
    packages = ['matpack'],
    description = "pacote de funções matemáticas únicas",
    long_description = "matpack é um pacote de funções matemáticas únicas desenvolvidas para facilitar a abordagem de diversos contextos",
    license = "MIT",
    keywords = "matematica, funções"

)