import numpy as np
import pandas as pd
from scipy import stats
from timeit import default_timer as timer

from density_utils import estimate_density

def trapezoid_sum(x, f):
    """
    Takes two arrays and computes the trapezoid sum of f(x) over the interval
    [min(x), max(x)]

    Parameters
    ----------
    x: array
       Subintevals bounds
    f: array
       The value of f(x) at each point in x

    Returns
    -------
    float
        Approximation of the integral given by the Riemann sum.
    """

    if not len(x) == len(f):
        raise ValueError("len(x) and len(f) must match")
    
    x_diff = x[1:] - x[:-1]
    f_midpoint = (f[1:] + f[:-1]) / 2

    return np.sum(f_midpoint * x_diff)

def get_estimator_func(
    bw="silverman",
    grid_len=256, 
    extend=True, 
    bound_correction=False, 
    adaptive=False,
    extend_fct=0.5, 
    bw_fct=1,
    bw_return=False,
    custom_lims=None
):
    
    def func(x):
        return estimate_density(x=x, bw=bw, grid_len=grid_len,
                       bound_correction=bound_correction,
                       adaptive=adaptive, extend_fct=extend_fct,
                       bw_fct=bw_fct, bw_return=bw_return,
                       custom_lims=custom_lims)
    return func

def get_gmixture_rvs(size, mean, sd, wt = None): 
    if wt is None:
        wt = np.repeat((1 / len(mean)), len(mean))
    assert len(mean) == len(sd) == len(wt)
    assert np.sum(wt) == 1
    x = np.concatenate((
        list(map(lambda m, s, w: stats.norm.rvs(m, s, int(np.round(size * w))), mean, sd, wt))
    ))
    return x

def get_gmixture_pdf(grid, mean, sd, wt=None):
    if wt is None:
        wt = np.repeat((1 / len(mean)), len(mean))
    assert len(mean) == len(sd) == len(wt)
    assert np.sum(wt) == 1
    pdf = np.average(list((map(lambda m, s: stats.norm.pdf(grid, m, s), mean, sd))), axis=0, weights=wt)
    return pdf

def get_gamma_rvs(size, shape, scale=1):
    return stats.gamma.rvs(a=shape, scale=scale, size=size)

def get_gamma_pdf(grid, shape, scale=1):
    return stats.gamma.pdf(grid, a=shape, scale=scale)

def get_logn_rvs(size, scale):
    return stats.lognorm.rvs(s=scale, size=size)

def get_logn_pdf(grid, scale):
    return stats.lognorm.pdf(grid, s=scale)

def get_beta_rvs(size, a, b):
    return stats.beta.rvs(a=b, b=b, size=size)

def get_beta_pdf(grid, a, b):
    return stats.beta.pdf(grid, a=a, b=b)

pdf_funcs = {
    "gaussian": get_gmixture_pdf,
    "gamma": get_gamma_pdf,
    "logn": get_logn_pdf,
    "beta": get_beta_pdf
}

rvs_funcs = {
    "gaussian": get_gmixture_rvs,
    "gamma": get_gamma_rvs,
    "logn": get_logn_rvs,
    "beta": get_beta_rvs
}

def get_funcs(identifier, **kwargs):
    
    def rvs_func(size):
        return rvs_funcs[identifier](size=size, **kwargs)
    
    def pdf_func(grid):
        return pdf_funcs[identifier](grid=grid, **kwargs)
    
    return rvs_func, pdf_func

def simulate(rvs_func, pdf_func, pdf_name, 
             estimator_func, estimator_name, 
             bw_name, sizes, niter=200):
    
    colums = ["iter", "pdf", "estimator", "bw", "size", "time", "error"]
    df = pd.DataFrame(columns=colums)
    loc = 0
    
    for size in sizes:
        for i in range(niter):
            
            # Generate sample
            rvs = rvs_func(size)

            # Estimate density and measure time
            start = timer()
            grid, pdf = estimator_func(rvs)
            end = timer()
            time = end - start

            # Estimate error
            squared_diff = (pdf - pdf_func(grid)) ** 2
            ise = trapezoid_sum(grid, squared_diff)
            
            # Append to data frame
            df.loc[loc] = [i + 1, pdf_name, estimator_name, bw_name, size, time, ise]
            loc += 1
        
    return df