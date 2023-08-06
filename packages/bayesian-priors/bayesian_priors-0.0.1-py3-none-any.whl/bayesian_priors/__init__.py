"""
Bayesian-priors is a package for visualizing prior distributions in the context of bayesian inference. The following continuous distributions are supported: normal, student-t, exponential, gamma, inverse gamma, weibull, pareto, gumbel, log-normal, cauchy, beta. In the dashboard, user inputs their desired lower and upper bounds, along with the % mass in-between. The dashboard will then display a set of  parameters that generates such distribution.
"""

from .prior_inverse_search import *
from .prior_dashboard_builder import dashboard

from . import blurb_normal
from . import blurb_studentt
from . import blurb_gumbel
from . import blurb_exponential
from . import blurb_gamma
from . import blurb_invgamma
from . import blurb_weibull
from . import blurb_pareto
from . import blurb_lognormal
from . import blurb_cauchy

__author__ = "Rosita Fu"
__version__ = "0.0.1"
__license__ = "MIT"
__email__ = "rosita.fu99@gmail.com"
