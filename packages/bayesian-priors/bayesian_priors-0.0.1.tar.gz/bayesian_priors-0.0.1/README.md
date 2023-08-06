
# bayesian_priors

A package for visualizing prior distributions in the context of Bayesian inference. The following continuous distributions are supported: *normal*, *student-t*, *exponential*, *gamma*, *inverse gamma*, *weibull*, *pareto*, *gumbel*, *log-normal*, *cauchy*, *beta*. Descriptions of the distributions are from https://distribution-explorer.github.io/. 





User inputs their desired lower and upper bounds along with the % mass in-between. The dashboard will then display a set of parameters that generates such distribution.

```shell
git clone https://github.com/atisor73/bayesian_priors.git
cd bayesian_priors/
python setup.py install    # install package
```

```python
import bayesian_priors

bayesian_priors.dashboard(description=True)
```



![](demo.png)
