import setuptools

# Required packages
normal_packages = [
    'bs4',
    'influxdb',
    'matplotlib',
    'numpy',
    'pandas',
    'sklearn',
    'statsmodels'
]
documentation_packages = [
    "sphinx",
    "sphinxcontrib-napoleon",
    "sphinxcontrib-programoutput"
]

setuptools.setup(name='bigforecast',
                 version='0.1',
                 description='Python functions used in orchestrating an always-on, self-updating macroeconomic forecasting engine',
                 url='https://github.com/jameslamb/repos/bigforecast',
                 packages=setuptools.find_packages(),
                 install_requires=normal_packages,
                 extras_requires={
                    'all': normal_packages + documentation_packages,
                    'docs': documentation_packages
                 },
                 zip_safe=False
                 )
