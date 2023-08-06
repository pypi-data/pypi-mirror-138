from setuptools import setup, find_packages

setup(
    name='hw3-CalCalc-fm',
    version='0.0.3',
    description='Calcalc module for hw3',
    long_description = "The module is created for homework-3 of course AY250 (Python Computing for Data Science) by Fanhao Meng. The main job that CalCalc.py does is to calculate your input string locally or from WolframAlpha API.",
    author='Fanhao Meng',
    author_email='fhmeng@berkeley.edu',
    keywords=['calculate', 'ay250', 'wolfram', 'homework'],
    packages=find_packages(),
    python_requires='>=3.6, <4',
    project_urls={
        'Source': 'https://github.com/fanhao-meng/python-ay250-homework',
    },
)