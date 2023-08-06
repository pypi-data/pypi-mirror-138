from setuptools import setup, find_packages

long_description = "Bayesian-priors is a package for visualizing prior distributions in the context of bayesian inference. The following continuous distributions are supported: normal, student-t, exponential, gamma, inverse gamma, weibull, pareto, gumbel, log-normal, cauchy, beta. In the dashboard, user inputs their desired lower and upper bounds, along with the % mass in-between. The dashboard will then display a set of  parameters that generates such distribution."

setup(
    name="bayesian_priors",
    version="0.0.1",
    description="Bayesian-priors is a package for visualizing prior distributions in the context of bayesian inference.",
    # url="https://github.com/atisor73/bayesian_priors",
    long_description=long_description,
    license="MIT",
    author='Rosita Fu',
    author_email='rosita.fu99@gmail.com',
    packages=find_packages(),
    install_requires=['numpy','scipy','pandas', 'bokeh','panel'],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ]
)
