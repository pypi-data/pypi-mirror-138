from setuptools import setup, find_packages


setup(
    name='fibonacci_ast_visualizer',
    version='0.3.2',
    author="Sergey Sokolvyak",
    packages=find_packages(where='src', include=['fibonacci_ast_visualizer', 'fibonacci_ast_visualizer.*']),
    package_dir={'': 'src'},
    url='https://github.com/zhvkgj/advance-python-itmo-2022',
    keywords='fibonacci, ast, networkx',
    install_requires=[
        'astunparse==1.6.3',
        'cycler==0.11.0',
        'fonttools==4.29.1',
        'kiwisolver==1.3.2',
        'matplotlib==3.5.1',
        'networkx==2.6.3',
        'numpy==1.22.1',
        'packaging==21.3',
        'Pillow==9.0.0',
        'pyparsing==3.0.7',
        'python-dateutil==2.8.2',
        'six==1.16.0'
      ]
)
