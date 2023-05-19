"""Spatial statistical tools to estimate uncertainties related to DEMs"""
from __future__ import annotations

import inspect
import itertools
import math as m
import multiprocessing as mp
import warnings
from typing import Any, Callable, Iterable, Literal, TypedDict, overload

import geopandas as gpd
import matplotlib
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numba
import numpy as np
import pandas as pd
from geoutils.georaster import Raster, RasterType
from geoutils.geovector import Vector, VectorType
from geoutils.spatial_tools import get_array_and_mask, subsample_raster
from numba import jit
from numpy.typing import ArrayLike
from scipy import integrate
from scipy.interpolate import RegularGridInterpolator, griddata
from scipy.optimize import curve_fit
from scipy.signal import fftconvolve
from scipy.spatial.distance import pdist, squareform
from scipy.stats import binned_statistic, binned_statistic_2d, binned_statistic_dd
from skimage.draw import disk

from xdem._typing import NDArrayf

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    import skgstat as skg


def nmad(data: NDArrayf, nfact: float = 1.4826) -> np.floating[Any]:
    """
    Calculate the normalized median absolute deviation (NMAD) of an array.
    Default scaling factor is 1.4826 to scale the median absolute deviation (MAD) to the dispersion of a normal
    distribution (see https://en.wikipedia.org/wiki/Median_absolute_deviation
    e.g. Höhle and Höhle (2009), http://dx.doi.org/10.1016/j.isprsjprs.2009.02.003)

    :param data: Input data
    :param nfact: Normalization factor for the data

    :returns nmad: (normalized) median absolute deviation of data.
    """
    if isinstance(data, np.ma.masked_array):
        data_arr = get_array_and_mask(data, check_shape=False)[0]
    else:
        data_arr = np.asarray(data)
    return nfact * np.nanmedian(np.abs(data_arr - np.nanmedian(data_arr)))


def nd_binning(
    values: NDArrayf,
    list_var: list[NDArrayf],
    list_var_names: list[str],
    list_var_bins: int | tuple[int, ...] | tuple[NDArrayf] | None = None,
    statistics: Iterable[str | Callable[[NDArrayf], np.floating[Any]]] = ("count", np.nanmedian, nmad),
    list_ranges: list[float] | None = None,
) -> pd.DataFrame:
    """
    N-dimensional binning of values according to one or several explanatory variables with computed statistics in
    each bin. By default, the sample count, the median and the normalized absolute median deviation (NMAD). The count
    is always computed, no matter user input.
    Values input is a (N,) array and variable input is a L-sized list of flattened arrays of similar dimensions (N,).
    For more details on the format of input variables, see documentation of scipy.stats.binned_statistic_dd.

    :param values: Values array of size (N,)
    :param list_var: List of size (L) of explanatory variables array of size (N,)
    :param list_var_names: List of size (L) of names of the explanatory variables
    :param list_var_bins: Count of size (1), or list of size (L) of counts or custom bin edges for the explanatory
        variables; defaults to 10 bins
    :param statistics: List of size (X) of statistics to be computed; defaults to count, median and nmad
    :param list_ranges: List of size (L) of minimum and maximum ranges to bin the explanatory variables; defaults to
        min/max of the data
    :return:
    """

    
    
    
    if list_var_bins is None:
        list_var_bins = (10,) * len(list_var_names)
    elif isinstance(list_var_bins, (int, np.integer)):
        list_var_bins = (list_var_bins,) * len(list_var_names)

    
    values = values.ravel()
    list_var = [var.ravel() for var in list_var]

    
    valid_data = np.logical_and.reduce([np.isfinite(values)] + [np.isfinite(var) for var in list_var])
    values = values[valid_data]
    list_var = [var[valid_data] for var in list_var]

    statistics = list(statistics)
    
    if "count" not in statistics:
        statistics.insert(0, "count")

    statistics_name = [f if isinstance(f, str) else f.__name__ for f in statistics]

    
    list_df_1d = []
    for i, var in enumerate(list_var):
        df_stats_1d = pd.DataFrame()
        
        for j, statistic in enumerate(statistics):
            stats_binned_1d, bedges_1d = binned_statistic(
                x=var, values=values, statistic=statistic, bins=list_var_bins[i], range=list_ranges
            )[:2]
            
            df_stats_1d[statistics_name[j]] = stats_binned_1d
        
        df_stats_1d[list_var_names[i]] = pd.IntervalIndex.from_breaks(bedges_1d, closed="left")
        
        df_stats_1d.insert(0, "nd", 1)

        list_df_1d.append(df_stats_1d)

    
    list_df_2d = []
    if len(list_var) > 1:
        combs = list(itertools.combinations(list_var_names, 2))
        for _, comb in enumerate(combs):
            var1_name, var2_name = comb
            
            i1, i2 = list_var_names.index(var1_name), list_var_names.index(var2_name)
            df_stats_2d = pd.DataFrame()
            for j, statistic in enumerate(statistics):
                stats_binned_2d, bedges_var1, bedges_var2 = binned_statistic_2d(
                    x=list_var[i1],
                    y=list_var[i2],
                    values=values,
                    statistic=statistic,
                    bins=[list_var_bins[i1], list_var_bins[i2]],
                    range=list_ranges,
                )[:3]
                
                df_stats_2d[statistics_name[j]] = stats_binned_2d.flatten()
            
            ii1 = pd.IntervalIndex.from_breaks(bedges_var1, closed="left")
            ii2 = pd.IntervalIndex.from_breaks(bedges_var2, closed="left")
            df_stats_2d[var1_name] = [i1 for i1 in ii1 for i2 in ii2]
            df_stats_2d[var2_name] = [i2 for i1 in ii1 for i2 in ii2]
            
            df_stats_2d.insert(0, "nd", 2)

            list_df_2d.append(df_stats_2d)

    
    df_stats_nd = pd.DataFrame()
    if len(list_var) > 2:
        for j, statistic in enumerate(statistics):
            stats_binned_2d, list_bedges = binned_statistic_dd(
                sample=list_var, values=values, statistic=statistic, bins=list_var_bins, range=list_ranges
            )[0:2]
            df_stats_nd[statistics_name[j]] = stats_binned_2d.flatten()
        list_ii = []
        
        for bedges in list_bedges:
            list_ii.append(pd.IntervalIndex.from_breaks(bedges, closed="left"))

        
        iind = np.meshgrid(*list_ii)
        for i, var_name in enumerate(list_var_names):
            df_stats_nd[var_name] = iind[i].flatten()

        
        df_stats_nd.insert(0, "nd", len(list_var_names))

    
    list_all_dfs = list_df_1d + list_df_2d + [df_stats_nd]
    df_concat = pd.concat(list_all_dfs)
    
    

    return df_concat


def interp_nd_binning(
    df: pd.DataFrame,
    list_var_names: str | list[str],
    statistic: str | Callable[[NDArrayf], np.floating[Any]] = nmad,
    min_count: int | None = 100,
) -> Callable[[tuple[ArrayLike, ...]], NDArrayf]:
    """
    Estimate an interpolant function for an N-dimensional binning. Preferably based on the output of nd_binning.
    For more details on the input dataframe, and associated list of variable name and statistic, see nd_binning.

    If the variable pd.DataSeries corresponds to an interval (as the output of nd_binning), uses the middle of the
    interval.
    Otherwise, uses the variable as such.

    Workflow of the function:
    Fills the no-data present on the regular N-D binning grid with nearest neighbour from scipy.griddata, then provides
    an interpolant function that linearly interpolates/extrapolates using scipy.RegularGridInterpolator.

    :param df: Dataframe with statistic of binned values according to explanatory variables
    :param list_var_names: Explanatory variable data series to select from the dataframe
    :param statistic: Statistic to interpolate, stored as a data series in the dataframe
    :param min_count: Minimum number of samples to be used as a valid statistic (replaced by nodata)
    :return: N-dimensional interpolant function

    :examples
    
    >>> df = pd.DataFrame({"var1": [1, 2, 3, 1, 2, 3, 1, 2, 3], "var2": [1, 1, 1, 2, 2, 2, 3, 3, 3],
    ... "statistic": [1, 2, 3, 4, 5, 6, 7, 8, 9]})

    
    
    
    
    
    
    >>> fun = interp_nd_binning(df, list_var_names=["var1", "var2"], statistic="statistic", min_count=None)

    
    >>> fun((2, 2))
    array(5.)

    
    >>> fun((1.5, 1.5))
    array(3.)

    
    >>> fun((-1, 1))
    array(-1.)
    """
    
    if isinstance(list_var_names, str):
        list_var_names = [list_var_names]

    
    for var in list_var_names:
        if var not in df.columns:
            raise ValueError('Variable "' + var + '" does not exist in the provided dataframe.')
    statistic_name = statistic if isinstance(statistic, str) else statistic.__name__
    if statistic_name not in df.columns:
        raise ValueError('Statistic "' + statistic_name + '" does not exist in the provided dataframe.')
    if min_count is not None and "count" not in df.columns:
        raise ValueError('Statistic "count" is not in the provided dataframe, necessary to use the min_count argument.')
    if df.empty:
        raise ValueError("Dataframe is empty.")

    df_sub = df.copy()

    
    if "nd" in df_sub.columns:
        df_sub = df_sub[df_sub.nd == len(list_var_names)]

    
    
    def to_interval(istr: str) -> float | pd.Interval:
        if isinstance(istr, float):
            return np.nan
        else:
            c_left = istr[0] == "["
            c_right = istr[-1] == "]"
            closed = {(True, False): "left", (False, True): "right", (True, True): "both", (False, False): "neither"}[
                c_left, c_right
            ]
            left, right = map(float, istr[1:-1].split(","))
            try:
                return pd.Interval(left, right, closed)
            except Exception:
                return np.nan

    
    for var in list_var_names:

        
        if all(isinstance(x, (int, float, np.integer, np.floating)) for x in df_sub[var].values):
            pass
        
        elif any(isinstance(x, pd.Interval) for x in df_sub[var].values):
            df_sub[var] = pd.IntervalIndex(df_sub[var]).mid.values
        
        
        elif any(isinstance(to_interval(x), pd.Interval) for x in df_sub[var].values):
            intervalindex_vals = [to_interval(x) for x in df_sub[var].values]
            df_sub[var] = pd.IntervalIndex(intervalindex_vals).mid.values
        else:
            raise ValueError("The variable columns must be provided as numerical mid values, or pd.Interval values.")

    
    df_sub = df_sub[np.logical_and.reduce([np.isfinite(df_sub[var].values) for var in list_var_names])]
    if df_sub.empty:
        raise ValueError(
            "Dataframe does not contain a nd binning with the variables corresponding to the list of variables."
        )
    
    if all(~np.isfinite(df_sub[statistic_name].values)):
        raise ValueError("Dataframe does not contain any valid statistic values.")

    
    if min_count is not None:
        df_sub.loc[df_sub["count"] < min_count, statistic_name] = np.nan

    values = df_sub[statistic_name].values
    ind_valid = np.isfinite(values)

    
    if all(~ind_valid):
        raise ValueError(
            "Dataframe does not contain any valid statistic values after filtering with min_count = "
            + str(min_count)
            + "."
        )

    
    list_bmid = []
    shape = []
    for var in list_var_names:
        bmid = sorted(np.unique(df_sub[var][ind_valid]))
        list_bmid.append(bmid)
        shape.append(len(bmid))

    
    
    values = values[ind_valid]
    
    points_valid = tuple(df_sub[var].values[ind_valid] for var in list_var_names)
    
    bmid_grid = np.meshgrid(*list_bmid, indexing="ij")
    points_grid = tuple(bmid_grid[i].flatten() for i in range(len(list_var_names)))
    
    values_grid = griddata(points_valid, values, points_grid, method="nearest")
    values_grid = values_grid.reshape(shape)

    
    
    interp_fun = RegularGridInterpolator(
        tuple(list_bmid), values_grid, method="linear", bounds_error=False, fill_value=None
    )

    return interp_fun  


def two_step_standardization(
    dvalues: NDArrayf,
    list_var: list[NDArrayf],
    unscaled_error_fun: Callable[[tuple[ArrayLike, ...]], NDArrayf],
    spread_statistic: Callable[[NDArrayf], np.floating[Any]] = nmad,
    fac_spread_outliers: float | None = 7,
) -> tuple[NDArrayf, Callable[[tuple[ArrayLike, ...]], NDArrayf]]:
    """
    Standardize the proxy differenced values using the modelled heteroscedasticity, re-scaled to the spread statistic,
    and generate the final standardization function.

    :param dvalues: Proxy values as array of size (N,) (i.e., differenced values where signal should be zero such as
        elevation differences on stable terrain)
    :param list_var: List of size (L) of explanatory variables array of size (N,)
    :param unscaled_error_fun: Function of the spread with explanatory variables not yet re-scaled
    :param spread_statistic: Statistic to be computed for the spread; defaults to nmad
    :param fac_spread_outliers: Exclude outliers outside this spread after standardizing; pass None to ignore.

    :return: Standardized values array of size (N,), Function to destandardize
    """

    
    zscores = dvalues / unscaled_error_fun(tuple(list_var))

    
    
    if fac_spread_outliers is not None:
        zscores[np.abs(zscores) > fac_spread_outliers * spread_statistic(zscores)] = np.nan

    
    
    zscore_nmad = spread_statistic(zscores)

    
    zscores /= zscore_nmad

    
    def error_fun(*args: tuple[ArrayLike, ...]) -> NDArrayf:
        return zscore_nmad * unscaled_error_fun(*args)

    return zscores, error_fun


def estimate_model_heteroscedasticity(
    dvalues: NDArrayf,
    list_var: list[NDArrayf],
    list_var_names: list[str],
    spread_statistic: Callable[[NDArrayf], np.floating[Any]] = nmad,
    list_var_bins: int | tuple[int, ...] | tuple[NDArrayf] | None = None,
    min_count: int | None = 100,
    fac_spread_outliers: float | None = 7,
) -> tuple[pd.DataFrame, Callable[[tuple[NDArrayf, ...]], NDArrayf]]:
    """
    Estimate and model the heteroscedasticity (i.e., variability in error) according to a list of explanatory variables
    from a proxy of differenced values (e.g., elevation differences), if possible compared to a source of higher
    precision.

    This function performs N-D data binning with the list of explanatory variable for a spread statistic, then
    performs N-D interpolation on this statistic, scales the output with a two-step standardization to return an error
    function of the explanatory variables.

    The functions used are `nd_binning`, `interp_nd_binning` and `two_step_standardization`.

    :param dvalues: Proxy values as array of size (N,) (i.e., differenced values where signal should be zero such as
        elevation differences on stable terrain)
    :param list_var: List of size (L) of explanatory variables array of size (N,)
    :param list_var_names: List of size (L) of names of the explanatory variables
    :param spread_statistic: Statistic to be computed for the spread; defaults to nmad
    :param list_var_bins: Count of size (1), or list of size (L) of counts or custom bin edges for the explanatory
        variables; defaults to 10 bins
    :param min_count: Minimum number of samples to be used as a valid statistic (replaced by nodata)
    :param fac_spread_outliers: Exclude outliers outside this spread after standardizing; pass None to ignore.

    :return: Dataframe of binned spread statistic with explanatory variables, Error function with explanatory variables
    """

    
    df = nd_binning(
        values=dvalues,
        list_var=list_var,
        list_var_names=list_var_names,
        statistics=[spread_statistic],
        list_var_bins=list_var_bins,
    )

    
    fun = interp_nd_binning(df, list_var_names=list_var_names, statistic=spread_statistic.__name__, min_count=min_count)

    
    final_fun = two_step_standardization(
        dvalues=dvalues,
        list_var=list_var,
        unscaled_error_fun=fun,
        spread_statistic=spread_statistic,
        fac_spread_outliers=fac_spread_outliers,
    )[1]

    return df, final_fun


@overload
def _preprocess_values_with_mask_to_array(  
    values: list[NDArrayf | RasterType],
    include_mask: NDArrayf | VectorType | gpd.GeoDataFrame = None,
    exclude_mask: NDArrayf | VectorType | gpd.GeoDataFrame = None,
    gsd: float | None = None,
    preserve_shape: bool = True,
) -> tuple[list[NDArrayf], float]:
    ...


@overload
def _preprocess_values_with_mask_to_array(
    values: NDArrayf | RasterType,
    include_mask: NDArrayf | VectorType | gpd.GeoDataFrame = None,
    exclude_mask: NDArrayf | VectorType | gpd.GeoDataFrame = None,
    gsd: float | None = None,
    preserve_shape: bool = True,
) -> tuple[NDArrayf, float]:
    ...


def _preprocess_values_with_mask_to_array(
    values: list[NDArrayf | RasterType] | NDArrayf | RasterType,
    include_mask: NDArrayf | VectorType | gpd.GeoDataFrame = None,
    exclude_mask: NDArrayf | VectorType | gpd.GeoDataFrame = None,
    gsd: float | None = None,
    preserve_shape: bool = True,
) -> tuple[list[NDArrayf] | NDArrayf, float]:
    """
    Preprocess input values provided as Raster or ndarray with a stable and/or unstable mask provided as Vector or
    ndarray into an array of stable values.

    By default, the shape is preserved and the masked values converted to NaNs.

    :param values: Values or list of values as a Raster, array or a list of Raster/arrays
    :param include_mask: Vector shapefile of mask to include (if values is Raster), or boolean array of same shape as
        values
    :param exclude_mask: Vector shapefile of mask to exclude (if values is Raster), or boolean array of same shape
        as values
    :param gsd: Ground sampling distance, if all the input values are provided as array
    :param preserve_shape: If True, masks unstable values with NaN. If False, returns a 1D array of stable values.

    :return: Array of stable terrain values, Ground sampling distance
    """

    
    if not isinstance(values, (Raster, np.ndarray, list)) or (
        isinstance(values, list) and not all(isinstance(val, (Raster, np.ndarray)) for val in values)
    ):
        raise ValueError("The values must be a Raster or NumPy array, or a list of those.")
    
    if include_mask is not None and not isinstance(include_mask, (np.ndarray, Vector, gpd.GeoDataFrame)):
        raise ValueError("The stable mask must be a Vector, GeoDataFrame or NumPy array.")
    if exclude_mask is not None and not isinstance(exclude_mask, (np.ndarray, Vector, gpd.GeoDataFrame)):
        raise ValueError("The unstable mask must be a Vector, GeoDataFrame or NumPy array.")

    
    if isinstance(values, list):
        any_raster = any(isinstance(val, Raster) for val in values)
    else:
        any_raster = isinstance(values, Raster)
    if not any_raster and isinstance(include_mask, (Vector, gpd.GeoDataFrame)):
        raise ValueError(
            "The stable mask can only passed as a Vector or GeoDataFrame if the input values contain a Raster."
        )

    
    if not isinstance(values, list):
        return_unlist = True
        values = [values]
    else:
        return_unlist = False

    
    values_arr = [get_array_and_mask(val)[0] if isinstance(val, Raster) else val for val in values]

    
    if gsd is None and any_raster:
        for i in range(len(values)):
            if isinstance(values[i], Raster):
                first_raster = values[i]
                break
        
        gsd = first_raster.res[0]  
    elif gsd is not None:
        gsd = gsd
    else:
        raise ValueError("The ground sampling distance must be provided if no Raster object is passed.")

    
    if include_mask is None:
        include_mask_arr = np.ones(np.shape(values_arr[0]), dtype=bool)
    elif isinstance(include_mask, (Vector, gpd.GeoDataFrame)):

        
        if isinstance(include_mask, gpd.GeoDataFrame):
            stable_vector = Vector(include_mask)
        else:
            stable_vector = include_mask

        
        include_mask_arr = stable_vector.create_mask(first_raster)
    
    else:
        include_mask_arr = include_mask

    
    if exclude_mask is None:
        exclude_mask_arr = np.zeros(np.shape(values_arr[0]), dtype=bool)
    elif isinstance(exclude_mask, (Vector, gpd.GeoDataFrame)):

        
        if isinstance(exclude_mask, gpd.GeoDataFrame):
            unstable_vector = Vector(exclude_mask)
        else:
            unstable_vector = exclude_mask

        
        exclude_mask_arr = unstable_vector.create_mask(first_raster)
    
    else:
        exclude_mask_arr = exclude_mask

    include_mask_arr = np.logical_and(include_mask_arr, ~exclude_mask_arr).squeeze()

    if preserve_shape:
        
        values_stable_arr = []
        for val in values_arr:
            val_stable = val.copy()
            val_stable[~include_mask_arr] = np.nan
            values_stable_arr.append(val_stable)
    else:
        values_stable_arr = [val_arr[include_mask_arr] for val_arr in values_arr]

    
    if return_unlist:
        values_stable_arr = values_stable_arr[0]

    return values_stable_arr, gsd


@overload
def infer_heteroscedasticity_from_stable(
    dvalues: NDArrayf,
    list_var: list[NDArrayf | RasterType],
    stable_mask: NDArrayf | VectorType | gpd.GeoDataFrame = None,
    unstable_mask: NDArrayf | VectorType | gpd.GeoDataFrame = None,
    list_var_names: list[str] = None,
    spread_statistic: Callable[[NDArrayf], np.floating[Any]] = nmad,
    list_var_bins: int | tuple[int, ...] | tuple[NDArrayf] | None = None,
    min_count: int | None = 100,
    fac_spread_outliers: float | None = 7,
) -> tuple[NDArrayf, pd.DataFrame, Callable[[tuple[NDArrayf, ...]], NDArrayf]]:
    ...


@overload
def infer_heteroscedasticity_from_stable(
    dvalues: RasterType,
    list_var: list[NDArrayf | RasterType],
    stable_mask: NDArrayf | VectorType | gpd.GeoDataFrame = None,
    unstable_mask: NDArrayf | VectorType | gpd.GeoDataFrame = None,
    list_var_names: list[str] = None,
    spread_statistic: Callable[[NDArrayf], np.floating[Any]] = nmad,
    list_var_bins: int | tuple[int, ...] | tuple[NDArrayf] | None = None,
    min_count: int | None = 100,
    fac_spread_outliers: float | None = 7,
) -> tuple[RasterType, pd.DataFrame, Callable[[tuple[NDArrayf, ...]], NDArrayf]]:
    ...


def infer_heteroscedasticity_from_stable(
    dvalues: NDArrayf | RasterType,
    list_var: list[NDArrayf | RasterType],
    stable_mask: NDArrayf | VectorType | gpd.GeoDataFrame = None,
    unstable_mask: NDArrayf | VectorType | gpd.GeoDataFrame = None,
    list_var_names: list[str] = None,
    spread_statistic: Callable[[NDArrayf], np.floating[Any]] = nmad,
    list_var_bins: int | tuple[int, ...] | tuple[NDArrayf] | None = None,
    min_count: int | None = 100,
    fac_spread_outliers: float | None = 7,
) -> tuple[NDArrayf | RasterType, pd.DataFrame, Callable[[tuple[NDArrayf, ...]], NDArrayf]]:
    """
    Infer heteroscedasticity from differenced values on stable terrain and a list of explanatory variables.

    This function returns an error map, a dataframe of spread values and the error function with explanatory variables.
    It is a convenience wrapper for `estimate_model_heteroscedasticity` to work on either Raster or array, compute the
    stable mask and return an error map.

    If no stable or unstable mask is provided to mask in or out the values, all terrain is used.

    :param dvalues: Proxy values as array or Raster (i.e., differenced values where signal should be zero such as
        elevation differences on stable terrain)
    :param list_var: List of size (L) of explanatory variables as array or Raster of same shape as dvalues
    :param stable_mask: Vector shapefile of stable terrain (if dvalues is Raster), or boolean array of same shape as
        dvalues
    :param unstable_mask: Vector shapefile of unstable terrain (if dvalues is Raster), or boolean array of same shape
        as dvalues
    :param list_var_names: List of size (L) of names of the explanatory variables, otherwise named var1, var2, etc.
    :param spread_statistic: Statistic to be computed for the spread; defaults to nmad
    :param list_var_bins: Count of size (1), or list of size (L) of counts or custom bin edges for the explanatory
        variables; defaults to 10 bins
    :param min_count: Minimum number of samples to be used as a valid statistic (replaced by nodata)
    :param fac_spread_outliers: Exclude outliers outside this spread after standardizing; pass None to ignore.

    :return: Inferred error map (array or Raster, same as input proxy values),
        Dataframe of binned spread statistic with explanatory variables,
        Error function with explanatory variables
    """

    
    if list_var_names is None:
        list_var_names = ["var" + str(i + 1) for i in range(len(list_var))]

    
    list_all_arr, gsd = _preprocess_values_with_mask_to_array(
        values=[dvalues] + list_var, include_mask=stable_mask, exclude_mask=unstable_mask, preserve_shape=False
    )
    dvalues_stable_arr = list_all_arr[0]
    list_var_stable_arr = list_all_arr[1:]

    
    df, fun = estimate_model_heteroscedasticity(
        dvalues=dvalues_stable_arr,
        list_var=list_var_stable_arr,
        list_var_names=list_var_names,
        spread_statistic=spread_statistic,
        list_var_bins=list_var_bins,
        min_count=min_count,
        fac_spread_outliers=fac_spread_outliers,
    )

    
    list_var_arr = [get_array_and_mask(var)[0] if isinstance(var, Raster) else var for var in list_var]
    error = fun(tuple(list_var_arr))

    
    if isinstance(dvalues, Raster):
        return dvalues.copy(new_array=error), df, fun
    else:
        return error, df, fun


def _create_circular_mask(
    shape: tuple[int, int], center: tuple[int, int] | None = None, radius: float | None = None
) -> NDArrayf:
    """
    Create circular mask on a raster, defaults to the center of the array and its half width

    :param shape: shape of array
    :param center: center
    :param radius: radius
    :return:
    """

    w, h = shape

    if center is None:  
        center = (int(w / 2), int(h / 2))
    if radius is None:  
        radius = min(center[0], center[1], w - center[0], h - center[1])

    
    mask = np.zeros(shape, dtype=bool)
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", "invalid value encountered in *divide")
        rr, cc = disk(center=center, radius=radius, shape=shape)
    mask[rr, cc] = True

    
    
    
    

    return mask


def _create_ring_mask(
    shape: tuple[int, int],
    center: tuple[int, int] | None = None,
    in_radius: float = 0,
    out_radius: float | None = None,
) -> NDArrayf:
    """
    Create ring mask on a raster, defaults to the center of the array and a circle mask of half width of the array

    :param shape: shape of array
    :param center: center
    :param in_radius: inside radius
    :param out_radius: outside radius
    :return:
    """

    w, h = shape

    if center is None:
        center = (int(w / 2), int(h / 2))
    if out_radius is None:
        out_radius = min(center[0], center[1], w - center[0], h - center[1])

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", "invalid value encountered in *divide")
        mask_inside = _create_circular_mask((w, h), center=center, radius=in_radius)
        mask_outside = _create_circular_mask((w, h), center=center, radius=out_radius)

    mask_ring = np.logical_and(~mask_inside, mask_outside)

    return mask_ring


def _random_state_definition(
    random_state: None | np.random.RandomState | int = None,
) -> np.random.RandomState | np.random.Generator:
    """
    Define random state based on input
    :param random_state: Random state or seed number to use for calculations (to fix random sampling during testing)
    :return:
    """

    if random_state is None:
        rnd: np.random.RandomState | np.random.Generator = np.random.default_rng()
    elif isinstance(random_state, np.random.RandomState):
        rnd = random_state
    else:
        rnd = np.random.RandomState(np.random.MT19937(np.random.SeedSequence(random_state)))

    return rnd


def _subsample_wrapper(
    values: NDArrayf,
    coords: NDArrayf,
    shape: tuple[int, int],
    subsample: int = 10000,
    subsample_method: str = "pdist_ring",
    inside_radius: float = 0,
    outside_radius: float = None,
    random_state: None | np.random.RandomState | int = None,
) -> tuple[NDArrayf, NDArrayf]:
    """
    (Not used by default)
    Wrapper for subsampling pdist methods
    """
    nx, ny = shape

    rnd = _random_state_definition(random_state=random_state)

    
    if subsample_method in ["pdist_disk", "pdist_ring"]:
        
        center_x = rnd.choice(nx, 1)[0]
        center_y = rnd.choice(ny, 1)[0]
        if subsample_method == "pdist_ring":
            subindex = _create_ring_mask(
                (nx, ny), center=(center_x, center_y), in_radius=inside_radius, out_radius=outside_radius
            )
        else:
            subindex = _create_circular_mask((nx, ny), center=(center_x, center_y), radius=outside_radius)

        index = subindex.flatten()
        values_sp = values[index]
        coords_sp = coords[index, :]

    else:
        values_sp = values
        coords_sp = coords

    index = subsample_raster(values_sp, subsample=subsample, return_indices=True, random_state=rnd)
    values_sub = values_sp[index[0]]
    coords_sub = coords_sp[index[0], :]

    return values_sub, coords_sub


def _aggregate_pdist_empirical_variogram(
    values: NDArrayf,
    coords: NDArrayf,
    subsample: int,
    shape: tuple[int, int],
    subsample_method: str,
    gsd: float,
    pdist_multi_ranges: list[float] | None = None,
    
    
    **kwargs: Any,
) -> pd.DataFrame:
    """
    (Not used by default)
    Aggregating subfunction of sample_empirical_variogram for pdist methods.
    The pairwise differences are calculated within each subsample.
    """

    
    if subsample_method in ["pdist_disk", "pdist_ring"]:

        if pdist_multi_ranges is None:

            
            pdist_multi_ranges = []
            
            new_range = gsd * 10
            while new_range < kwargs.get("maxlag") / 2:  
                pdist_multi_ranges.append(new_range)
                new_range *= 2
            pdist_multi_ranges.append(kwargs.get("maxlag"))  

        
        list_inside_radius = []
        list_outside_radius: list[float | None] = []
        binned_ranges = [0.0] + pdist_multi_ranges
        for i in range(len(binned_ranges) - 1):

            
            outside_radius = binned_ranges[i + 1] / gsd
            if subsample_method == "pdist_ring":
                inside_radius = binned_ranges[i] / gsd
            else:
                inside_radius = 0.0

            list_outside_radius.append(outside_radius)
            list_inside_radius.append(inside_radius)
    else:
        
        pdist_multi_ranges = [kwargs.get("maxlag")]  
        list_outside_radius = [None]
        list_inside_radius = [0.0]

    
    list_df_range = []
    for j in range(len(pdist_multi_ranges)):

        values_sub, coords_sub = _subsample_wrapper(
            values,
            coords,
            shape=shape,
            subsample=subsample,
            subsample_method=subsample_method,
            inside_radius=list_inside_radius[j],
            outside_radius=list_outside_radius[j],
            random_state=kwargs.get("random_state"),
        )
        if len(values_sub) == 0:
            continue
        df_range = _get_pdist_empirical_variogram(values=values_sub, coords=coords_sub, **kwargs)

        
        list_df_range.append(df_range)

    df = pd.concat(list_df_range)

    return df


def _get_pdist_empirical_variogram(values: NDArrayf, coords: NDArrayf, **kwargs: Any) -> pd.DataFrame:
    """
    Get empirical variogram from skgstat.Variogram object calculating pairwise distances within the sample

    :param values: Values
    :param coords: Coordinates
    :return: Empirical variogram (variance, upper bound of lag bin, counts)

    """

    
    kwargs.pop("random_state")

    
    variogram_args = skg.Variogram.__init__.__code__.co_varnames[: skg.Variogram.__init__.__code__.co_argcount]
    
    remaining_kwargs = kwargs.copy()
    for arg in variogram_args:
        remaining_kwargs.pop(arg, None)
    if len(remaining_kwargs) != 0:
        warnings.warn("Keyword arguments: " + ",".join(list(remaining_kwargs.keys())) + " were not used.")
    
    filtered_kwargs = {k: kwargs[k] for k in variogram_args if k in kwargs}

    
    V = skg.Variogram(coordinates=coords, values=values, normalize=False, fit_method=None, **filtered_kwargs)

    
    bins, exp = V.get_empirical()
    count = V.bin_count

    
    df = pd.DataFrame()
    df = df.assign(exp=exp, bins=bins, count=count)

    return df


def _choose_cdist_equidistant_sampling_parameters(**kwargs: Any) -> tuple[int, int, float]:
    """
    Add a little calculation to partition the "subsample" argument automatically into the "run" and "samples"
    arguments of RasterEquidistantMetricSpace, to have a similar number of points than with a classic pdist method.

    We compute the arguments to match a N0**2/2 number of pairwise comparison, N0 being the "subsample" input, and
    forcing the number of rings to 10 by default. This corresponds to 10 independent rings with equal number of samples
    compared pairwise against a central disk. We force this number of sample to be at least 2 (skgstat raises an error
    if there is only one). Additionally, if samples permit, we compute 10 independent runs, maximum 100 to limit
    processing times when aggregating different runs in sparse matrixes. If even more sample permit (default case), we
    increase the number of subsamples in rings and runs simultaneously.

    The number of pairwise samples for a classic pdist is N0(N0-1)/2 with N0 the number of samples of the ensemble. For
    the cdist equidistant calculation it is M*N*R where N are the subsamples in the center disk, M is the number of
    samples in the rings which amounts to X*N where X is the number of rings in the grid extent, as each ring draws N
    samples. And R is the number of runs with a different random center point.
    X is fixed by the extent and ratio_subsample parameters, and so N0**2/2 = R*X*N**2, and we want at least 10 rings
    and, if possible, 10 runs.

    !! Different variables: !! The "samples" of RasterEquidistantMetricSpace is N, while the "subsample" passed is N0.
    """

    
    extent = kwargs["extent"]
    shape = kwargs["shape"]
    subsample = kwargs["subsample"]

    
    
    if "nb_rings" in kwargs.keys():
        nb_rings = kwargs["nb_rings"]
    else:
        nb_rings = 10
    
    
    min_subsample = np.ceil(np.sqrt(2 * nb_rings * 2**2) + 1)
    if subsample < min_subsample:
        raise ValueError(f"The number of subsamples needs to be at least {min_subsample:.0f}.")

    
    pairwise_comp_per_disk = np.ceil(subsample**2 / (2 * nb_rings))

    
    
    if pairwise_comp_per_disk < 10:
        runs = int(pairwise_comp_per_disk / 2**2)
    else:
        runs = int(min(100, 10 * np.ceil((pairwise_comp_per_disk / (2**2 * 10)) ** (1 / 3))))

    
    subsample_per_disk_per_run = int(np.ceil(np.sqrt(pairwise_comp_per_disk / runs)))

    

    
    maxdist = np.sqrt((extent[1] - extent[0]) ** 2 + (extent[3] - extent[2]) ** 2)
    res = np.mean([(extent[1] - extent[0]) / (shape[0] - 1), (extent[3] - extent[2]) / (shape[1] - 1)])

    
    
    
    
    ratio_subsample = res**2 * subsample_per_disk_per_run / (np.pi * maxdist**2 / np.sqrt(2) ** (2 * nb_rings))

    
    total_pairwise_comparison = runs * subsample_per_disk_per_run**2 * nb_rings

    if kwargs["verbose"]:
        print(
            "Equidistant circular sampling will be performed for {} runs (random center points) with pairwise "
            "comparison between {} samples (points) of the central disk and again {} samples times {} independent "
            "rings centered on the same center point. This results in approximately {} pairwise comparisons (duplicate"
            " pairwise points randomly selected will be removed).".format(
                runs, subsample_per_disk_per_run, subsample_per_disk_per_run, nb_rings, total_pairwise_comparison
            )
        )

    return runs, subsample_per_disk_per_run, ratio_subsample


def _get_cdist_empirical_variogram(
    values: NDArrayf, coords: NDArrayf, subsample_method: str, **kwargs: Any
) -> pd.DataFrame:
    """
    Get empirical variogram from skgstat.Variogram object calculating pairwise distances between two sample collections
    of a MetricSpace (see scikit-gstat documentation for more details)

    :param values: Values
    :param coords: Coordinates
    :return: Empirical variogram (variance, upper bound of lag bin, counts)

    """

    if subsample_method == "cdist_equidistant" and "runs" not in kwargs.keys() and "samples" not in kwargs.keys():

        
        "subsample" with pdist, except if those parameters are already user-defined
        runs, samples, ratio_subsample = _choose_cdist_equidistant_sampling_parameters(**kwargs)

        kwargs["runs"] = runs
        "samples" argument is used by skgstat Metric subclasses (and not "subsample")
        kwargs["samples"] = samples
        kwargs["ratio_subsample"] = ratio_subsample
        kwargs.pop("subsample")

    elif subsample_method == "cdist_point":

        
        kwargs["samples"] = kwargs.pop("subsample")

    "random_state" argument into "rnd", also used by skgstat Metric subclasses
    kwargs["rnd"] = kwargs.pop("random_state")

    
    if subsample_method == "cdist_point":
        
        ms_args = skg.ProbabalisticMetricSpace.__init__.__code__.co_varnames[
            : skg.ProbabalisticMetricSpace.__init__.__code__.co_argcount
        ]
        ms = skg.ProbabalisticMetricSpace
    else:
        
        ms_args = skg.RasterEquidistantMetricSpace.__init__.__code__.co_varnames[
            : skg.RasterEquidistantMetricSpace.__init__.__code__.co_argcount
        ]
        ms = skg.RasterEquidistantMetricSpace

    
    variogram_args = skg.Variogram.__init__.__code__.co_varnames[: skg.Variogram.__init__.__code__.co_argcount]
    
    remaining_kwargs = kwargs.copy()
    for arg in variogram_args + ms_args:
        remaining_kwargs.pop(arg, None)
    if len(remaining_kwargs) != 0:
        warnings.warn("Keyword arguments: " + ", ".join(list(remaining_kwargs.keys())) + " were not used.")

    
    filtered_ms_kwargs = {k: kwargs[k] for k in ms_args if k in kwargs}
    M = ms(coords=coords, **filtered_ms_kwargs)

    
    filtered_var_kwargs = {k: kwargs[k] for k in variogram_args if k in kwargs}
    V = skg.Variogram(M, values=values, normalize=False, fit_method=None, **filtered_var_kwargs)

    
    bins, exp = V.get_empirical(bin_center=False)
    count = V.bin_count

    
    df = pd.DataFrame()
    df = df.assign(exp=exp, bins=bins, count=count)

    return df


def _wrapper_get_empirical_variogram(argdict: dict[str, Any]) -> pd.DataFrame:
    """
    Multiprocessing wrapper for get_pdist_empirical_variogram and get_cdist_empirical variogram

    :param argdict: Keyword argument to pass to get_pdist/cdist_empirical_variogram
    :return: Empirical variogram (variance, upper bound of lag bin, counts)

    """
    if argdict["verbose"]:
        print("Working on run " + str(argdict["i"]) + " out of " + str(argdict["imax"]))
    argdict.pop("i")
    argdict.pop("imax")

    if argdict["subsample_method"] in ["cdist_equidistant", "cdist_point"]:
        
        return _get_cdist_empirical_variogram(**argdict)
    else:
        
        return _aggregate_pdist_empirical_variogram(**argdict)


class EmpiricalVariogramKArgs(TypedDict, total=False):
    runs: int
    pdist_multi_ranges: list[float]
    ratio_subsample: float
    samples: int
    nb_rings: int
    maxlag: float
    bin_func: Any
    estimator: str


def sample_empirical_variogram(
    values: NDArrayf | RasterType,
    gsd: float = None,
    coords: NDArrayf = None,
    subsample: int = 1000,
    subsample_method: str = "cdist_equidistant",
    n_variograms: int = 1,
    n_jobs: int = 1,
    verbose: bool = False,
    random_state: None | np.random.RandomState | int = None,
    
    
    **kwargs: int | list[float] | float | str | Any,
) -> pd.DataFrame:
    """
    Sample empirical variograms with binning adaptable to multiple ranges and spatial subsampling adapted for raster
    data.
    Returns an empirical variogram (empirical variance, upper bound of spatial lag bin, count of pairwise samples).

    If values are provided as a Raster subclass, nothing else is required.
    If values are provided as a 2D array (M,N), a ground sampling distance is sufficient to derive the pairwise
    distances.
    If values are provided as a 1D array (N), an array of coordinates (N,2) or (2,N) is expected. If the coordinates
    do not correspond to points of a grid, a ground sampling distance is needed to correctly get the grid size.

    By default, the subsampling is based on RasterEquidistantMetricSpace implemented in scikit-gstat. This method
    samples more effectively large grid data by isolating pairs of spatially equidistant ensembles for distributed
    pairwise comparison. In practice, two subsamples are drawn for pairwise comparison: one from a disk of certain
    radius within the grid, and another one from rings of larger radii that increase steadily between the pixel size
    and the extent of the raster. Those disks and rings are sampled several times across the grid using random centers.
    See more details in Hugonnet et al. (2022), https://doi.org/10.1109/jstars.2022.3188922, in particular on
    Supplementary Fig. 13. for the subsampling scheme.

    The "subsample" argument determines the number of samples for each method to yield a number of pairwise comparisons
    close to that of a pdist calculation, that is N*(N-1)/2 where N is the subsample argument.
    For the cdist equidistant method, the "runs" (random centers) and "samples" (subsample of a disk/ring) are set
    automatically to get close to N*(N-1)/2 pairwise samples, fixing a number of rings "nb_rings" to 10. Those can be
    more finely adjusted by passing the argument "runs", "samples" and "nb_rings" to kwargs. Further details can be
    found in the description of skgstat.MetricSpace.RasterEquidistantMetricSpace or
    _choose_cdist_equidistant_sampling_parameters.

    Spatial subsampling method argument subsample_method can be one of "cdist_equidistant", "cdist_point",
    "pdist_point", "pdist_disk" and "pdist_ring".
    The cdist methods use MetricSpace classes of scikit-gstat and do pairwise comparison between two distinct ensembles
    as in scipy.spatial.cdist. For the cdist methods, the variogram is estimated in a single run from the MetricSpace.

    The pdist methods use methods to subsample the Raster points directly and do pairwise comparison within a single
    ensemble as in scipy.spatial.pdist. For the pdist methods, an iterative process is required: a list of ranges
    subsampled independently is used.

    Variograms are derived independently for several runs and ranges using each pairwise sample, and later aggregated.
    If the subsampling method selected is "random_point", the multi-range argument is ignored as range has no effect on
    this subsampling method.

    For pdist methods, keyword arguments are passed to skgstat.Variogram.
    For cdist methods, keyword arguments are passed to both skgstat.Variogram and skgstat.MetricSpace.

    :param values: Values of studied variable
    :param gsd: Ground sampling distance
    :param coords: Coordinates
    :param subsample: Number of samples to randomly draw from the values
    :param subsample_method: Spatial subsampling method
    :param n_variograms: Number of independent empirical variogram estimations (to estimate empirical variogram spread)
    :param n_jobs: Number of processing cores
    :param verbose: Print statements during processing
    :param random_state: Random state or seed number to use for calculations (to fix random sampling during testing)

    :return: Empirical variogram (variance, upper bound of lag bin, counts)
    """
    
    if isinstance(values, Raster):
        gsd = values.res[0]
        values, mask = get_array_and_mask(values)
    elif isinstance(values, (np.ndarray, np.ma.masked_array)):
        values, mask = get_array_and_mask(values)
    else:
        raise ValueError("Values must be of type NDArrayf, np.ma.masked_array or Raster subclass.")
    values = values.squeeze()

    
    if (gsd is not None or subsample_method in ["cdist_equidistant", "pdist_disk", "pdist_ring"]) and values.ndim == 1:
        raise ValueError(
            'Values array must be 2D when using any of the "cdist_equidistant", "pdist_disk" and '
            '"pdist_ring" methods, or providing a ground sampling distance instead of coordinates.'
        )
    elif coords is not None and values.ndim != 1:
        raise ValueError("Values array must be 1D when providing coordinates.")
    elif coords is not None and (coords.shape[0] != 2 and coords.shape[1] != 2):
        raise ValueError("The coordinates array must have one dimension with length equal to 2")
    elif values.ndim == 2 and gsd is None:
        raise ValueError("The ground sampling distance must be defined when passing a 2D values array.")

    
    if subsample_method not in ["cdist_equidistant", "cdist_point", "pdist_point", "pdist_disk", "pdist_ring"]:
        raise TypeError(
            'The subsampling method must be one of "cdist_equidistant, "cdist_point", "pdist_point", '
            '"pdist_disk" or "pdist_ring".'
        )
    
    
    if n_variograms > 1 and "bin_func" in kwargs.keys() and not isinstance(kwargs.get("bin_func"), Iterable):
        warnings.warn(
            "Using a named binning function of scikit-gstat might provide different binnings for each "
            "independent run. To remediate that issue, pass bin_func as an Iterable of right bin edges, "
            "(or use default bin_func)."
        )

    
    if coords is not None:
        nx = None
        ny = None
        
        if coords.shape[0] == 2 and coords.shape[1] != 2:
            coords = np.transpose(coords)
    
    
    else:
        nx, ny = np.shape(values)
        x, y = np.meshgrid(np.arange(0, values.shape[0] * gsd, gsd), np.arange(0, values.shape[1] * gsd, gsd))
        coords = np.dstack((x.flatten(), y.flatten())).squeeze()
        values = values.flatten()

    
    if gsd is None:
        gsd = np.mean([coords[0, 0] - coords[0, 1], coords[0, 0] - coords[1, 0]])
    
    extent = (np.min(coords[:, 0]), np.max(coords[:, 0]), np.min(coords[:, 1]), np.max(coords[:, 1]))

    
    if "maxlag" not in kwargs.keys():
        
        
        maxlag = np.sqrt(
            (np.max(coords[:, 0]) - np.min(coords[:, 0])) ** 2 + (np.max(coords[:, 1]) - np.min(coords[:, 1])) ** 2
        )
        kwargs.update({"maxlag": maxlag})

    
    if "cdist" in subsample_method:
        ind_valid = np.isfinite(values)
        values = values[ind_valid]
        coords = coords[ind_valid, :]

    if "bin_func" not in kwargs.keys():
        
        
        bin_func = []
        right_bin_edge = np.sqrt(2) * gsd
        while right_bin_edge < kwargs.get("maxlag"):
            bin_func.append(right_bin_edge)
            
            right_bin_edge *= np.sqrt(2)
        bin_func.append(kwargs.get("maxlag"))
        kwargs.update({"bin_func": bin_func})

    
    args = {
        "values": values,
        "coords": coords,
        "subsample_method": subsample_method,
        "subsample": subsample,
        "verbose": verbose,
    }
    if subsample_method in ["cdist_equidistant", "pdist_ring", "pdist_disk", "pdist_point"]:
        
        args.update({"shape": (nx, ny)})
        if subsample_method == "cdist_equidistant":
            
            args.update({"extent": extent})
        else:
            args.update({"gsd": gsd})

    
    
    if random_state is not None:
        
        if isinstance(random_state, np.random.RandomState):
            rnd = random_state
        elif isinstance(random_state, np.random.Generator):
            rnd = np.random.RandomState(random_state)
        else:
            rnd = np.random.RandomState(np.random.MT19937(np.random.SeedSequence(random_state)))

        
        if n_variograms == 1:
            
            list_random_state: list[None | np.random.RandomState] = [rnd]
        else:
            
            list_random_state = list(rnd.choice(n_variograms, n_variograms, replace=False))
    else:
        list_random_state = [None for i in range(n_variograms)]

    
    
    
    if n_jobs == 1:
        if verbose:
            print("Using 1 core...")

        list_df_run = []
        for i in range(n_variograms):

            argdict = {
                "i": i,
                "imax": n_variograms,
                "random_state": list_random_state[i],
                **args,
                **kwargs,  
            }
            df_run = _wrapper_get_empirical_variogram(argdict=argdict)

            list_df_run.append(df_run)
    else:
        if verbose:
            print("Using " + str(n_jobs) + " cores...")

        pool = mp.Pool(n_jobs, maxtasksperchild=1)
        list_argdict = [
            {"i": i, "imax": n_variograms, "random_state": list_random_state[i], **args, **kwargs}  
            for i in range(n_variograms)
        ]
        list_df_run = pool.map(_wrapper_get_empirical_variogram, list_argdict, chunksize=1)
        pool.close()
        pool.join()

    
    df = pd.concat(list_df_run)

    
    if n_variograms == 1:
        df = df.rename(columns={"bins": "lags"})
        df["err_exp"] = np.nan
    
    else:
        df_grouped = df.groupby("bins", dropna=False)
        df_mean = df_grouped[["exp"]].mean()
        df_std = df_grouped[["exp"]].std()
        df_count = df_grouped[["count"]].sum()
        df_mean["lags"] = df_mean.index.values
        df_mean["err_exp"] = df_std["exp"] / np.sqrt(n_variograms)
        df_mean["count"] = df_count["count"]
        df = df_mean

    
    df.drop(df.tail(1).index, inplace=True)

    
    df = df.astype({"exp": "float64", "err_exp": "float64", "lags": "float64", "count": "int64"})

    return df


def _get_skgstat_variogram_model_name(model: str | Callable[[NDArrayf, float, float], NDArrayf]) -> str:
    """Function to identify a SciKit-GStat variogram model from a string or a function"""

    list_supported_models = ["spherical", "gaussian", "exponential", "cubic", "stable", "matern"]

    if callable(model):
        if inspect.getmodule(model).__name__ == "skgstat.models":  
            model_name = model.__name__
        else:
            raise ValueError("Variogram models can only be passed as functions of the skgstat.models package.")

    elif isinstance(model, str):
        model_name = "None"
        for supp_model in list_supported_models:
            if model.lower() in [supp_model[0:3], supp_model]:
                model_name = supp_model.lower()
        if model_name == "None":
            raise ValueError(
                f"Variogram model name {model} not recognized. Supported models are: "
                + ", ".join(list_supported_models)
                + "."
            )

    else:
        raise ValueError(
            "Variogram models can be passed as strings or skgstat.models function. "
            "Supported models are: " + ", ".join(list_supported_models) + "."
        )

    return model_name


def get_variogram_model_func(params_variogram_model: pd.DataFrame) -> Callable[[NDArrayf], NDArrayf]:
    """
    Construct the sum of spatial variogram function from a dataframe of variogram parameters.

    :param params_variogram_model: Dataframe of variogram models to sum with three to four columns, "model" for the
        model types (e.g., ["spherical", "matern"]), "range" for the correlation ranges (e.g., [2, 100]), "psill" for
        the partial sills (e.g., [0.8, 0.2]) and "smooth" for the smoothness parameter if it exists for this model
        (e.g., [None, 0.2]).

    :return: Function of sum of variogram with spatial lags.
    """

    
    _check_validity_params_variogram(params_variogram_model)

    
    def sum_model(h: NDArrayf) -> NDArrayf:

        fn = np.zeros(np.shape(h))

        for i in range(len(params_variogram_model)):
            
            model_name = _get_skgstat_variogram_model_name(params_variogram_model["model"].values[i])
            model_function = getattr(skg.models, model_name)
            r = params_variogram_model["range"].values[i]
            p = params_variogram_model["psill"].values[i]
            
            if model_name in ["spherical", "gaussian", "exponential", "cubic"]:
                fn += model_function(h, r, p)
            
            elif model_name in ["stable", "matern"]:
                s = params_variogram_model["smooth"].values[i]
                fn += model_function(h, r, p, s)
        return fn

    return sum_model


def covariance_from_variogram(params_variogram_model: pd.DataFrame) -> Callable[[NDArrayf], NDArrayf]:
    """
    Construct the spatial covariance function from a dataframe of variogram parameters.
    The covariance function is the sum of partial sills "PS" minus the sum of associated variograms "gamma":
    C = PS - gamma

    :param params_variogram_model: Dataframe of variogram models to sum with three to four columns, "model" for the
        model types (e.g., ["spherical", "matern"]), "range" for the correlation ranges (e.g., [2, 100]), "psill" for
        the partial sills (e.g., [0.8, 0.2]) and "smooth" for the smoothness parameter if it exists for this model
        (e.g., [None, 0.2]).

    :return: Covariance function with spatial lags
    """

    
    _check_validity_params_variogram(params_variogram_model)

    
    total_sill = np.sum(params_variogram_model["psill"])

    
    sum_variogram = get_variogram_model_func(params_variogram_model)

    def cov(h: NDArrayf) -> NDArrayf:
        return total_sill - sum_variogram(h)

    return cov


def correlation_from_variogram(params_variogram_model: pd.DataFrame) -> Callable[[NDArrayf], NDArrayf]:
    """
    Construct the spatial correlation function from a dataframe of variogram parameters.
    The correlation function is the covariance function "C" divided by the sum of partial sills "PS": rho = C / PS

    :param params_variogram_model: Dataframe of variogram models to sum with three to four columns, "model" for the
        model types (e.g., ["spherical", "matern"]), "range" for the correlation ranges (e.g., [2, 100]), "psill" for
        the partial sills (e.g., [0.8, 0.2]) and "smooth" for the smoothness parameter if it exists for this model
        (e.g., [None, 0.2]).

    :return: Correlation function with spatial lags
    """

    
    _check_validity_params_variogram(params_variogram_model)

    
    total_sill = np.sum(params_variogram_model["psill"].values)

    
    cov = covariance_from_variogram(params_variogram_model)

    def rho(h: NDArrayf) -> NDArrayf:
        return cov(h) / total_sill

    return rho


def fit_sum_model_variogram(
    list_models: list[str | Callable[[NDArrayf, float, float], NDArrayf]],
    empirical_variogram: pd.DataFrame,
    bounds: list[tuple[float, float]] = None,
    p0: list[float] = None,
) -> tuple[Callable[[NDArrayf], NDArrayf], pd.DataFrame]:
    """
    Fit a sum of variogram models to an empirical variogram, with weighted least-squares based on sampling errors. To
    use preferably with the empirical variogram dataframe returned by the `sample_empirical_variogram` function.

    :param list_models: List of K variogram models to sum for the fit in order from short to long ranges. Can either be
        a 3-letter string, full string of the variogram name or SciKit-GStat model function (e.g., for a
        spherical model "Sph", "Spherical" or skgstat.models.spherical).
    :param empirical_variogram: Empirical variogram, formatted as a dataframe with count (pairwise sample count), lags
        (upper bound of spatial lag bin), exp (experimental variance), and err_exp (error on experimental variance).
    :param bounds: Bounds of range and sill parameters for each model (shape K x 4 = K x range lower, range upper, sill
        lower, sill upper).
    :param p0: Initial guess of ranges and sills each model (shape K x 2 = K x range first guess, sill first guess).

    :return: Function of sum of variogram, Dataframe of optimized coefficients.
    """

    
    def variogram_sum(h: float, *args: list[float]) -> float:
        fn = 0.0
        i = 0
        for model in list_models:
            
            model_name = _get_skgstat_variogram_model_name(model)
            model_function = getattr(skg.models, model_name)
            
            if model_name in ["spherical", "gaussian", "exponential", "cubic"]:
                fn += model_function(h, args[i], args[i + 1])
                i += 2
            
            elif model_name in ["stable", "matern"]:
                fn += model_function(h, args[i], args[i + 1], args[i + 2])
                i += 3

        return fn

    
    empirical_variogram = empirical_variogram[np.isfinite(empirical_variogram.exp.values)]

    
    n_average = np.ceil(len(empirical_variogram.exp.values) / 10)
    exp_movaverage = np.convolve(empirical_variogram.exp.values, np.ones(int(n_average)) / n_average, mode="valid")
    
    max_var = np.max(exp_movaverage)

    
    if bounds is None:
        bounds = [(0, empirical_variogram.lags.values[-1]), (0, max_var)] * len(list_models)

    if p0 is None:
        p0 = []
        for i in range(len(list_models)):
            
            psill_p0 = ((i + 1) / len(list_models)) * max_var

            
            
            
            
            range_p0 = ((i + 1) / len(list_models)) * empirical_variogram.lags.values[-1]

            p0.append(range_p0)
            p0.append(psill_p0)

    final_bounds = np.transpose(np.array(bounds))

    
    if np.all(np.isnan(empirical_variogram.err_exp.values)) or np.all(empirical_variogram.err_exp.values == 0):
        cof, cov = curve_fit(
            variogram_sum,
            empirical_variogram.lags.values,
            empirical_variogram.exp.values,
            method="trf",
            p0=p0,
            bounds=final_bounds,
        )
    
    else:
        
        valid = np.isfinite(empirical_variogram.err_exp.values)
        cof, cov = curve_fit(
            variogram_sum,
            empirical_variogram.lags.values[valid],
            empirical_variogram.exp.values[valid],
            method="trf",
            p0=p0,
            bounds=final_bounds,
            sigma=empirical_variogram.err_exp.values[valid],
        )

    
    list_df = []
    i = 0
    for model in list_models:
        model_name = _get_skgstat_variogram_model_name(model)
        
        if model_name in ["spherical", "gaussian", "exponential", "cubic"]:
            df = pd.DataFrame()
            df = df.assign(model=[model_name], range=[cof[i]], psill=[cof[i + 1]])
            i += 2
        
        elif model_name in ["stable", "matern"]:
            df = pd.DataFrame()
            df = df.assign(model=[model_name], range=[cof[i]], psill=[cof[i + 1]], smooth=[cof[i + 2]])
            i += 3
        list_df.append(df)
    df_params = pd.concat(list_df)

    
    variogram_sum_fit = get_variogram_model_func(df_params)

    return variogram_sum_fit, df_params


def estimate_model_spatial_correlation(
    dvalues: NDArrayf | RasterType,
    list_models: list[str | Callable[[NDArrayf, float, float], NDArrayf]],
    estimator: str = "dowd",
    gsd: float = None,
    coords: NDArrayf = None,
    subsample: int = 1000,
    subsample_method: str = "cdist_equidistant",
    n_variograms: int = 1,
    n_jobs: int = 1,
    verbose: bool = False,
    random_state: None | np.random.RandomState | int = None,
    bounds: list[tuple[float, float]] = None,
    p0: list[float] = None,
    **kwargs: Any,
) -> tuple[pd.DataFrame, pd.DataFrame, Callable[[NDArrayf], NDArrayf]]:

    """
    Estimate and model the spatial correlation of the input variable by empirical variogram sampling and fitting of a
    sum of variogram model.

    The spatial correlation is returned as a function of spatial lags (in units of the input coordinates) which gives a
    correlation value between 0 and 1.

    This function samples an empirical variogram using skgstat.Variogram, then optimizes by weighted least-squares the
    sum of a defined number of models, using the functions `sample_empirical_variogram` and `fit_sum_model_variogram`.

    :param dvalues: Proxy values as array or Raster (i.e., differenced values where signal should be zero such as
        elevation differences on stable terrain)
    :param list_models: List of K variogram models to sum for the fit in order from short to long ranges. Can either be
        a 3-letter string, full string of the variogram name or SciKit-GStat model function (e.g., for a
        spherical model "Sph", "Spherical" or skgstat.models.spherical).
    :param estimator: Estimator for the empirical variogram; default to Dowd's variogram (see skgstat.Variogram for
        the list of available estimators).
    :param gsd: Ground sampling distance
    :param coords: Coordinates
    :param subsample: Number of samples to randomly draw from the values
    :param subsample_method: Spatial subsampling method
    :param n_variograms: Number of independent empirical variogram estimations (to estimate empirical variogram spread)
    :param n_jobs: Number of processing cores
    :param verbose: Print statements during processing
    :param random_state: Random state or seed number to use for calculations (to fix random sampling during testing)
    :param bounds: Bounds of range and sill parameters for each model (shape K x 4 = K x range lower, range upper,
        sill lower, sill upper).
    :param p0: Initial guess of ranges and sills each model (shape K x 2 = K x range first guess, sill first guess).

    :return: Dataframe of empirical variogram, Dataframe of optimized model parameters, Function of spatial correlation
        (0 to 1) with spatial lags
    """

    empirical_variogram = sample_empirical_variogram(
        values=dvalues,
        estimator=estimator,
        gsd=gsd,
        coords=coords,
        subsample=subsample,
        subsample_method=subsample_method,
        n_variograms=n_variograms,
        n_jobs=n_jobs,
        verbose=verbose,
        random_state=random_state,
        **kwargs,
    )

    params_variogram_model = fit_sum_model_variogram(
        list_models=list_models, empirical_variogram=empirical_variogram, bounds=bounds, p0=p0
    )[1]

    spatial_correlation_func = correlation_from_variogram(params_variogram_model=params_variogram_model)

    return empirical_variogram, params_variogram_model, spatial_correlation_func


def infer_spatial_correlation_from_stable(
    dvalues: NDArrayf | RasterType,
    list_models: list[str | Callable[[NDArrayf, float, float], NDArrayf]],
    stable_mask: NDArrayf | VectorType | gpd.GeoDataFrame = None,
    unstable_mask: NDArrayf | VectorType | gpd.GeoDataFrame = None,
    errors: NDArrayf | RasterType = None,
    estimator: str = "dowd",
    gsd: float = None,
    coords: NDArrayf = None,
    subsample: int = 1000,
    subsample_method: str = "cdist_equidistant",
    n_variograms: int = 1,
    n_jobs: int = 1,
    verbose: bool = False,
    bounds: list[tuple[float, float]] = None,
    p0: list[float] = None,
    random_state: None | np.random.RandomState | int = None,
    **kwargs: Any,
) -> tuple[pd.DataFrame, pd.DataFrame, Callable[[NDArrayf], NDArrayf]]:
    """
    Infer spatial correlation of errors from differenced values on stable terrain and a list of variogram model to fit
    as a sum.

    This function returns a dataframe of the empirical variogram, a dataframe of optimized model parameters, and a
    spatial correlation function. The spatial correlation is returned as a function of spatial lags
    (in units of the input coordinates) which gives a correlation value between 0 and 1.
    It is a convenience wrapper for `estimate_model_spatial_correlation` to work on either Raster or array and compute
    the stable mask.

    If no stable or unstable mask is provided to mask in or out the values, all terrain is used.

    :param dvalues: Proxy values as array or Raster (i.e., differenced values where signal should be zero such as
        elevation differences on stable terrain)
    :param list_models: List of K variogram models to sum for the fit in order from short to long ranges. Can either be
        a 3-letter string, full string of the variogram name or SciKit-GStat model function (e.g., for a
        spherical model "Sph", "Spherical" or skgstat.models.spherical).
    :param stable_mask: Vector shapefile of stable terrain (if dvalues is Raster), or boolean array of same shape as
        dvalues
    :param unstable_mask: Vector shapefile of unstable terrain (if dvalues is Raster), or boolean array of same shape
        as dvalues
    :param errors: Error values to account for heteroscedasticity (ignored if None).
    :param estimator: Estimator for the empirical variogram; default to Dowd's variogram (see skgstat.Variogram for
        the list of available estimators).
    :param gsd: Ground sampling distance, if input values are provided as array
    :param coords: Coordinates
    :param subsample: Number of samples to randomly draw from the values
    :param subsample_method: Spatial subsampling method
    :param n_variograms: Number of independent empirical variogram estimations (to estimate empirical variogram spread)
    :param n_jobs: Number of processing cores
    :param verbose: Print statements during processing
    :param bounds: Bounds of range and sill parameters for each model (shape K x 4 = K x range lower, range upper,
        sill lower, sill upper).
    :param p0: Initial guess of ranges and sills each model (shape K x 2 = K x range first guess, sill first guess).
    :param random_state: Random state or seed number to use for calculations (to fix random sampling during testing)

    :return: Dataframe of empirical variogram, Dataframe of optimized model parameters, Function of spatial correlation
        (0 to 1) with spatial lags
    """

    dvalues_stable_arr, gsd = _preprocess_values_with_mask_to_array(
        values=dvalues, include_mask=stable_mask, exclude_mask=unstable_mask, gsd=gsd
    )

    
    if errors is not None:
        if isinstance(errors, Raster):
            errors_arr = get_array_and_mask(errors)[0]
        else:
            errors_arr = errors

        
        dvalues_stable_arr /= errors_arr

    
    empirical_variogram, params_variogram_model, spatial_correlation_func = estimate_model_spatial_correlation(
        dvalues=dvalues_stable_arr,
        list_models=list_models,
        estimator=estimator,
        gsd=gsd,
        coords=coords,
        subsample=subsample,
        subsample_method=subsample_method,
        n_variograms=n_variograms,
        n_jobs=n_jobs,
        verbose=verbose,
        random_state=random_state,
        bounds=bounds,
        p0=p0,
        **kwargs,
    )

    return empirical_variogram, params_variogram_model, spatial_correlation_func


def _check_validity_params_variogram(params_variogram_model: pd.DataFrame) -> None:
    """Check the validity of the modelled variogram parameters dataframe (mostly in the case it is passed manually)."""

    
    expected_columns = ["model", "range", "psill"]
    if not all(c in params_variogram_model for c in expected_columns):
        raise ValueError(
            'The dataframe with variogram parameters must contain the columns "model", "range" and "psill".'
        )

    
    for model in params_variogram_model["model"].values:
        _get_skgstat_variogram_model_name(model)

    
    for r in params_variogram_model["range"].values:
        if not isinstance(r, (float, np.floating, int, np.integer)):
            raise ValueError("The variogram ranges must be float or integer.")
        if r <= 0:
            raise ValueError("The variogram ranges must have non-zero, positive values.")

    
    for p in params_variogram_model["psill"].values:
        if not isinstance(p, (float, np.floating, int, np.integer)):
            raise ValueError("The variogram partial sills must be float or integer.")
        if p <= 0:
            raise ValueError("The variogram partial sills must have non-zero, positive values.")

    
    if ["stable"] in params_variogram_model["model"].values or ["matern"] in params_variogram_model["model"].values:
        if "smooth" not in params_variogram_model:
            raise ValueError(
                'The dataframe with variogram parameters must contain the column "smooth" for '
                "the smoothness factor when using Matern or Stable models."
            )
        for i in range(len(params_variogram_model)):
            if params_variogram_model["model"].values[i] in ["stable", "matern"]:
                s = params_variogram_model["smooth"].values[i]
                if not isinstance(s, (float, np.floating, int, np.integer)):
                    raise ValueError("The variogram smoothness parameter must be float or integer.")
                if s <= 0:
                    raise ValueError("The variogram smoothness parameter must have non-zero, positive values.")


def neff_circular_approx_theoretical(area: float, params_variogram_model: pd.DataFrame) -> float:
    """
    Number of effective samples approximated from exact disk integration of a sum of any number of variogram models
    of spherical, gaussian, exponential or cubic form over a disk of a certain area. This approximation performs best
    for areas with a shape close to that of a disk.
    Inspired by Rolstad et al. (2009): http://dx.doi.org/10.3189/002214309789470950.
    The input variogram parameters match the format of the dataframe returned by `fit_sum_variogram_models`, also
    detailed in the parameter description to be passed manually.

    This function contains the exact integrated formulas and is mostly used for testing the numerical integration
    of any number and forms of variograms provided by the function `neff_circular_approx_numerical`.

    The number of effective samples serves to convert between standard deviation and standard error. For example, with
    two models: if SE is the standard error, SD the standard deviation and N_eff the number of effective samples:
    SE = SD / sqrt(N_eff) => N_eff = SD^2 / SE^2 => N_eff = (PS1 + PS2)/SE^2 where PS1 and PS2 are the partial sills
    estimated from the variogram models, and SE is estimated by integrating the variogram models with parameters PS1/PS2
    and R1/R2 where R1/R2 are the correlation ranges.

    :param area: Area (in square unit of the variogram ranges)
    :param params_variogram_model: Dataframe of variogram models to sum with three to four columns, "model" for the
        model types (e.g., ["spherical", "matern"]), "range" for the correlation ranges (e.g., [2, 100]), "psill" for
        the partial sills (e.g., [0.8, 0.2]) and "smooth" for the smoothness parameter if it exists for this model
        (e.g., [None, 0.2]).

    :return: Number of effective samples
    """

    
    _check_validity_params_variogram(params_variogram_model)

    
    l_equiv = np.sqrt(area / np.pi)

    

    
    

    
    
    
    
    
    

    def spherical_exact_integral(a1: float, c1: float, L: float) -> float:
        if l_equiv <= a1:
            squared_se = c1 * (1 - L / a1 + 1 / 5 * (L / a1) ** 3)
        else:
            squared_se = c1 / 5 * (a1 / L) ** 2
        return squared_se

    
    

    def exponential_exact_integral(a1: float, c1: float, L: float) -> float:
        a = a1 / 3
        squared_se = 2 * c1 * (a / L) ** 2 * (1 - np.exp(-L / a) * (1 + L / a))
        return squared_se

    
    

    def gaussian_exact_integral(a1: float, c1: float, L: float) -> float:
        a = a1 / 2
        squared_se = c1 * (a / L) ** 2 * (1 - np.exp(-(L**2) / a**2))
        return squared_se

    
    
    
    

    def cubic_exact_integral(a1: float, c1: float, L: float) -> float:
        if l_equiv <= a1:
            squared_se = (
                c1
                * (6 * a1**7 - 21 * a1**5 * L**2 + 21 * a1**4 * L**3 - 6 * a1**2 * L**5 + L**7)
                / (6 * a1**7)
            )
        else:
            squared_se = 1 / 6 * c1 * a1**2 / L**2
        return squared_se

    squared_se = 0.0
    valid_models = ["spherical", "exponential", "gaussian", "cubic"]
    exact_integrals = [
        spherical_exact_integral,
        exponential_exact_integral,
        gaussian_exact_integral,
        cubic_exact_integral,
    ]
    for i in np.arange(len(params_variogram_model)):
        model_name = _get_skgstat_variogram_model_name(params_variogram_model["model"].values[i])
        r = params_variogram_model["range"].values[i]
        p = params_variogram_model["psill"].values[i]
        if model_name in valid_models:
            exact_integral = exact_integrals[valid_models.index(model_name)]
            squared_se += exact_integral(r, p, l_equiv)

    
    total_sill = np.nansum(params_variogram_model.psill)
    
    neff = total_sill / squared_se

    return neff


def _integrate_fun(fun: Callable[[NDArrayf], NDArrayf], low_b: float, upp_b: float) -> float:
    """
    Numerically integrate function between an upper and lower bounds
    :param fun: Function to integrate
    :param low_b: Lower bound
    :param upp_b: Upper bound

    :return: Integral between lower and upper bound
    """
    return integrate.quad(fun, low_b, upp_b)[0]


def neff_circular_approx_numerical(area: float | int, params_variogram_model: pd.DataFrame) -> float:
    """
    Number of effective samples derived from numerical integration for any sum of variogram models over a circular area.
    This is a generalization of Rolstad et al. (2009): http://dx.doi.org/10.3189/002214309789470950, which is verified
    against exact integration of `neff_circular_approx_theoretical`. This approximation performs best for areas with
    a shape close to that of a disk.
    The input variogram parameters match the format of the dataframe returned by `fit_sum_variogram_models`, also
    detailed in the parameter description to be passed manually.

    The number of effective samples N_eff serves to convert between standard deviation and standard error
    over the area: SE = SD / sqrt(N_eff) if SE is the standard error, SD the standard deviation.

    :param area: Area (in square unit of the variogram ranges)
    :param params_variogram_model: Dataframe of variogram models to sum with three to four columns, "model" for the
        model types (e.g., ["spherical", "matern"]), "range" for the correlation ranges (e.g., [2, 100]), "psill" for
        the partial sills (e.g., [0.8, 0.2]) and "smooth" for the smoothness parameter if it exists for this model
        (e.g., [None, 0.2]).

    :returns: Number of effective samples
    """

    
    _check_validity_params_variogram(params_variogram_model)

    
    total_sill = np.nansum(params_variogram_model.psill)

    
    def hcov_sum(h: NDArrayf) -> NDArrayf:
        return h * covariance_from_variogram(params_variogram_model)(h)

    
    h_equiv = np.sqrt(area / np.pi)

    
    full_int = _integrate_fun(hcov_sum, 0, h_equiv)

    
    squared_se = 2 * np.pi * full_int / area

    
    neff = total_sill / squared_se

    return neff


def neff_exact(
    coords: NDArrayf, errors: NDArrayf, params_variogram_model: pd.DataFrame, vectorized: bool = True
) -> float:
    """
     Exact number of effective samples derived from a double sum of covariance with euclidean coordinates based on
     the provided variogram parameters. This method works for any shape of area.

    :param coords: Center coordinates with size (N,2) for each spatial support (typically, pixel)
    :param errors: Errors at the coordinates with size (N,) for each spatial support (typically, pixel)
    :param params_variogram_model: Dataframe of variogram models to sum with three to four columns, "model" for the
        model types (e.g., ["spherical", "matern"]), "range" for the correlation ranges (e.g., [2, 100]), "psill" for
        the partial sills (e.g., [0.8, 0.2]) and "smooth" for the smoothness parameter if it exists for this model
        (e.g., [None, 0.2]).
    :param vectorized: Perform the vectorized calculation (used for testing).

    :return: Number of effective samples
    """

    
    _check_validity_params_variogram(params_variogram_model)

    
    rho = correlation_from_variogram(params_variogram_model)

    
    n = len(coords)
    pds = pdist(coords)

    
    
    if not vectorized:
        var = 0.0
        for i in range(n):
            for j in range(n):

                
                
                if i == j:
                    d = 0
                elif i < j:
                    ind = n * i + j - ((i + 2) * (i + 1)) // 2
                    d = pds[ind]
                else:
                    ind = n * j + i - ((j + 2) * (j + 1)) // 2
                    d = pds[ind]

                var += rho(d) * errors[i] * errors[j]  

    
    else:
        
        pds_matrix = squareform(pds)
        
        var = np.sum(
            errors.reshape((-1, 1)) @ errors.reshape((1, -1)) * rho(pds_matrix.flatten()).reshape(pds_matrix.shape)
        )

    
    squared_se_dsc = var / n**2
    neff = np.mean(errors) ** 2 / squared_se_dsc

    return neff


def neff_hugonnet_approx(
    coords: NDArrayf,
    errors: NDArrayf,
    params_variogram_model: pd.DataFrame,
    subsample: int = 1000,
    vectorized: bool = True,
    random_state: None | np.random.RandomState | int = None,
) -> float:
    """
    Approximated number of effective samples derived from a double sum of covariance subsetted on one of the two sums,
    based on euclidean coordinates with the provided variogram parameters. This method works for any shape of area.
    See Hugonnet et al. (2022), https://doi.org/10.1109/jstars.2022.3188922, in particular Supplementary Fig. S16.

    :param coords: Center coordinates with size (N,2) for each spatial support (typically, pixel)
    :param errors: Errors at the coordinates with size (N,) for each spatial support (typically, pixel)
    :param params_variogram_model: Dataframe of variogram models to sum with three to four columns, "model" for the
        model types (e.g., ["spherical", "matern"]), "range" for the correlation ranges (e.g., [2, 100]), "psill" for
        the partial sills (e.g., [0.8, 0.2]) and "smooth" for the smoothness parameter if it exists for this model
        (e.g., [None, 0.2]).
    :param subsample: Number of samples to subset the calculation
    :param vectorized: Perform the vectorized calculation (used for testing).
    :param random_state: Random state or seed number to use for calculations (to fix random sampling during testing)

    :return: Number of effective samples
    """

    
    rnd = _random_state_definition(random_state=random_state)

    
    _check_validity_params_variogram(params_variogram_model)

    
    rho = correlation_from_variogram(params_variogram_model)

    
    n = len(coords)
    pds = pdist(coords)

    
    subsample = min(subsample, n)

    
    rand_points = rnd.choice(n, size=subsample, replace=False)

    
    
    if not vectorized:
        var = 0.0
        for ind_sub in range(subsample):
            for j in range(n):

                i = rand_points[ind_sub]
                
                
                if i == j:
                    d = 0
                elif i < j:
                    ind = n * i + j - ((i + 2) * (i + 1)) // 2
                    d = pds[ind]
                else:
                    ind = n * j + i - ((j + 2) * (j + 1)) // 2
                    d = pds[ind]

                var += rho(d) * errors[i] * errors[j]  

    
    else:
        
        errors_sub = errors[rand_points]
        pds_matrix = squareform(pds)
        pds_matrix_sub = pds_matrix[:, rand_points]
        
        var = np.sum(
            errors.reshape((-1, 1))
            @ errors_sub.reshape((1, -1))
            * rho(pds_matrix_sub.flatten()).reshape(pds_matrix_sub.shape)
        )

    
    squared_se_dsc = var / (n * subsample)
    neff = np.mean(errors) ** 2 / squared_se_dsc

    return neff


def number_effective_samples(
    area: float | int | VectorType | gpd.GeoDataFrame,
    params_variogram_model: pd.DataFrame,
    rasterize_resolution: RasterType | float = None,
    **kwargs: Any,
) -> float:
    """
    Compute the number of effective samples, i.e. the number of uncorrelated samples, in an area accounting for spatial
    correlations described by a sum of variogram models.

    This function wraps two methods:

    - A discretized integration method that provides the exact estimate for any shape of area using a double sum of
        covariance. By default, this method is approximated using Equation 18 of Hugonnet et al. (2022),
        https://doi.org/10.1109/jstars.2022.3188922 to decrease computing times while preserving a good approximation.

    - A continuous integration method that provides a conservative (i.e., slightly overestimated) value for a disk
        area shape, based on a generalization of the approach of Rolstad et al. (2009),
        http://dx.doi.org/10.3189/002214309789470950.

    By default, if a numeric value is passed for an area, the continuous method is used considering a disk shape. If a
    vector is passed, the discretized method is computed on that shape. If the discretized method is used, a resolution
    for rasterization is generally expected, otherwise is arbitrarily chosen as a fifth of the shortest correlation
    range to ensure a sufficiently fine grid for propagation of the shortest range.

    :param area: Area of interest either as a numeric value of surface in the same unit as the variogram ranges (will
        assume a circular shape), or as a vector (shapefile) of the area
    :param params_variogram_model: Dataframe of variogram models to sum with three to four columns, "model" for the
        model types (e.g., ["spherical", "matern"]), "range" for the correlation ranges (e.g., [2, 100]), "psill" for
        the partial sills (e.g., [0.8, 0.2]) and "smooth" for the smoothness parameter if it exists for this model
        (e.g., [None, 0.2]).
    :param rasterize_resolution: Resolution to rasterize the area if passed as a vector. Can be a float value or a
        Raster.
    :param kwargs: Keyword argument to pass to the `neff_hugonnet_approx` function.

    :return: Number of effective samples
    """

    
    _check_validity_params_variogram(params_variogram_model=params_variogram_model)

    
    if isinstance(area, (float, int)):
        neff = neff_circular_approx_numerical(area=area, params_variogram_model=params_variogram_model)

    
    elif isinstance(area, (Vector, gpd.GeoDataFrame)):

        
        if isinstance(area, gpd.GeoDataFrame):
            V = Vector(area)
        else:
            V = area

        if rasterize_resolution is None:
            rasterize_resolution = np.min(params_variogram_model["range"].values) / 5.0
            warnings.warn(
                "Resolution for vector rasterization is not defined and thus set at 20% of the shortest "
                "correlation range, which might result in large memory usage."
            )

        
        if isinstance(rasterize_resolution, (float, int, np.floating, np.integer)):

            
            mask = V.create_mask(xres=rasterize_resolution)
            x = rasterize_resolution * np.arange(0, mask.shape[0])
            y = rasterize_resolution * np.arange(0, mask.shape[1])
            coords = np.array(np.meshgrid(y, x))
            coords_on_mask = coords[:, mask].T

        elif isinstance(rasterize_resolution, Raster):

            
            mask = V.create_mask(rst=rasterize_resolution).squeeze()
            coords = np.array(rasterize_resolution.coords())
            coords_on_mask = coords[:, mask].T

        else:
            raise ValueError("The rasterize resolution must be a float, integer or Raster subclass.")

        
        errors_on_mask = np.ones(len(coords_on_mask))

        neff = neff_hugonnet_approx(
            coords=coords_on_mask, errors=errors_on_mask, params_variogram_model=params_variogram_model, **kwargs
        )

    else:
        raise ValueError("Area must be a float, integer, Vector subclass or geopandas dataframe.")

    return neff


def spatial_error_propagation(
    areas: list[float | VectorType | gpd.GeoDataFrame],
    errors: RasterType,
    params_variogram_model: pd.Dataframe,
    **kwargs: Any,
) -> list[float]:
    """
    Spatial propagation of elevation errors to an area using the estimated heteroscedasticity and spatial correlations.

    This function is based on the `number_effective_samples` function to estimate uncorrelated samples. If given a
    vector area, it uses Equation 18 of Hugonnet et al. (2022), https://doi.org/10.1109/jstars.2022.3188922. If given
    a numeric area, it uses a generalization of Rolstad et al. (2009), http://dx.doi.org/10.3189/002214309789470950.

    The standard error SE (1-sigma) is then computed as SE = mean(SD) / Neff, where mean(SD) is the mean of errors in
    the area of interest which accounts for heteroscedasticity, and Neff is the number of effective samples.

    :param areas: Area of interest either as a numeric value of surface in the same unit as the variogram ranges (will
        assume a circular shape), or as a vector (shapefile) of the area.
    :param errors: Errors from heteroscedasticity estimation and modelling, as an array or Raster.
    :param params_variogram_model: Dataframe of variogram models to sum with three to four columns, "model" for the
        model types (e.g., ["spherical", "matern"]), "range" for the correlation ranges (e.g., [2, 100]), "psill" for
        the partial sills (e.g., [0.8, 0.2]) and "smooth" for the smoothness parameter if it exists for this model
        (e.g., [None, 0.2]).
    :param kwargs: Keyword argument to pass to the `neff_hugonnet_approx` function.

    :return: List of standard errors (1-sigma) for the input areas
    """

    standard_errors = []
    errors_arr = get_array_and_mask(errors)[0]
    for area in areas:
        
        neff = number_effective_samples(
            area=area, params_variogram_model=params_variogram_model, rasterize_resolution=errors, **kwargs
        )

        
        
        if isinstance(area, float):
            average_spread = np.nanmean(errors_arr)
        else:
            if isinstance(area, gpd.GeoDataFrame):
                area_vector = Vector(area)
            else:
                area_vector = area
            area_mask = area_vector.create_mask(errors).squeeze()

            average_spread = np.nanmean(errors_arr[area_mask])

        
        standard_error = average_spread / np.sqrt(neff)
        standard_errors.append(standard_error)

    return standard_errors


def _std_err_finite(std: float, neff_tot: float, neff: float) -> float:
    """
    Standard error formula for a subsample of a finite ensemble.

    :param std: standard deviation
    :param neff_tot: maximum number of effective samples
    :param neff: number of effective samples

    :return: standard error
    """
    return std * np.sqrt(1 / neff_tot * (neff_tot - neff) / neff_tot)


def _std_err(std: float, neff: float) -> float:
    """
    Standard error formula.

    :param std: standard deviation
    :param neff: number of effective samples

    :return: standard error
    """
    return std * np.sqrt(1 / neff)


def _distance_latlon(tup1: tuple[float, float], tup2: tuple[float, float], earth_rad: float = 6373000) -> float:
    """
    Distance between two lat/lon coordinates projected on a spheroid
    ref: https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
    :param tup1: lon/lat coordinates of first point
    :param tup2: lon/lat coordinates of second point
    :param earth_rad: radius of the earth in meters

    :return: distance
    """
    lat1 = m.radians(abs(tup1[1]))
    lon1 = m.radians(abs(tup1[0]))
    lat2 = m.radians(abs(tup2[1]))
    lon2 = m.radians(abs(tup2[0]))

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = m.sin(dlat / 2) ** 2 + m.cos(lat1) * m.cos(lat2) * m.sin(dlon / 2) ** 2
    c = 2 * m.atan2(m.sqrt(a), m.sqrt(1 - a))

    distance = earth_rad * c

    return distance


def _scipy_convolution(imgs: NDArrayf, filters: NDArrayf, output: NDArrayf) -> None:
    """
    Scipy convolution on a number n_N of 2D images of size N1 x N2 using a number of kernels n_M of sizes M1 x M2.

    :param imgs: Input array of size (n_N, N1, N2) with n_N images of size N1 x N2
    :param filters: Input array of filters of size (n_M, M1, M2) with n_M filters of size M1 x M2
    :param output: Initialized output array of size (n_N, n_M, N1, N2)
    """

    for i_N in np.arange(imgs.shape[0]):
        for i_M in np.arange(filters.shape[0]):
            output[i_N, i_M, :, :] = fftconvolve(imgs[i_N, :, :], filters[i_M, :, :], mode="same")


nd4type = numba.double[:, :, :, :]
nd3type = numba.double[:, :, :]


@jit((nd3type, nd3type, nd4type))  
def _numba_convolution(imgs: NDArrayf, filters: NDArrayf, output: NDArrayf) -> None:
    """
    Numba convolution on a number n_N of 2D images of size N1 x N2 using a number of kernels n_M of sizes M1 x M2.

    :param imgs: Input array of size (n_N, N1, N2) with n_N images of size N1 x N2
    :param filters: Input array of filters of size (n_M, M1, M2) with n_M filters of size M1 x M2
    :param output: Initialized output array of size (n_N, n_M, N1, N2)
    """
    n_rows, n_cols, n_imgs = imgs.shape
    height, width, n_filters = filters.shape

    for ii in range(n_imgs):
        for rr in range(n_rows - height + 1):
            for cc in range(n_cols - width + 1):
                for hh in range(height):
                    for ww in range(width):
                        for ff in range(n_filters):
                            imgval = imgs[rr + hh, cc + ww, ii]
                            filterval = filters[hh, ww, ff]
                            output[rr, cc, ii, ff] += imgval * filterval


def convolution(imgs: NDArrayf, filters: NDArrayf, method: str = "scipy") -> NDArrayf:
    """
    Convolution on a number n_N of 2D images of size N1 x N2 using a number of kernels n_M of sizes M1 x M2, using
    either scipy.signal.fftconvolve or accelerated numba loops.
    Note that the indexes on n_M and n_N correspond to first axes on the array to speed up computations (prefetching).
    Inspired by: https://laurentperrinet.github.io/sciblog/posts/2017-09-20-the-fastest-2d-convolution-in-the-world.html

    :param imgs: Input array of size (n_N, N1, N2) with n_N images of size N1 x N2
    :param filters: Input array of filters of size (n_M, M1, M2) with n_M filters of size M1 x M2
    :param method: Method to perform the convolution: "scipy" or "numba"

    :return: Filled array of outputs of size (n_N, n_M, N1, N2)
    """

    
    n_N, N1, N2 = imgs.shape
    n_M, M1, M2 = filters.shape
    output = np.zeros((n_N, n_M, N1, N2))

    if method.lower() == "scipy":
        _scipy_convolution(imgs=imgs, filters=filters, output=output)
    elif method.lower() == "numba":
        _numba_convolution(
            imgs=imgs.astype(dtype=np.double),
            filters=filters.astype(dtype=np.double),
            output=output.astype(dtype=np.double),
        )
    else:
        raise ValueError('Method must be "scipy" or "numba".')

    return output


def mean_filter_nan(
    img: NDArrayf, kernel_size: int, kernel_shape: str = "circular", method: str = "scipy"
) -> tuple[NDArrayf, NDArrayf, int]:
    """
    Apply a mean filter to an image with a square or circular kernel of size p and with NaN values ignored.

    :param img: Input array of size (N1, N2)
    :param kernel_size: Size M of kernel, which will be a symmetrical (M, M) kernel
    :param kernel_shape: Shape of kernel, either "square" or "circular"
    :param method: Method to perform the convolution: "scipy" or "numba"

    :return: Array of size (N1, N2) with mean values, Array of size (N1, N2) with number of valid pixels, Number of
        pixels in the kernel
    """

    
    p = kernel_size

    
    img_zeroed = img.copy()
    img_zeroed[~np.isfinite(img_zeroed)] = 0

    
    if kernel_shape.lower() == "square":
        kernel = np.ones((p, p), dtype="uint8")

    
    elif kernel_shape.lower() == "circular":
        kernel = _create_circular_mask((p, p)).astype("uint8")
    else:
        raise ValueError('Kernel shape should be "square" or "circular".')

    
    summed_img = convolution(
        imgs=img_zeroed.reshape((1, img_zeroed.shape[0], img_zeroed.shape[1])),
        filters=kernel.reshape((1, kernel.shape[0], kernel.shape[1])),
        method=method,
    ).squeeze()

    
    nodata_img = np.ones(np.shape(img), dtype=np.int8)
    nodata_img[~np.isfinite(img)] = 0

    
    nb_valid_img = convolution(
        imgs=nodata_img.reshape((1, nodata_img.shape[0], nodata_img.shape[1])),
        filters=kernel.reshape((1, kernel.shape[0], kernel.shape[1])),
        method=method,
    ).squeeze()

    
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", "divide by zero encountered in *divide")
        mean_img = summed_img / nb_valid_img

    
    nb_pixel_per_kernel = np.count_nonzero(kernel)

    return mean_img, nb_valid_img, nb_pixel_per_kernel


def _patches_convolution(
    values: NDArrayf,
    gsd: float,
    area: float,
    perc_min_valid: float = 80.0,
    patch_shape: str = "circular",
    method: str = "scipy",
    statistic_between_patches: Callable[[NDArrayf], np.floating[Any]] = nmad,
    verbose: bool = False,
    return_in_patch_statistics: bool = False,
) -> tuple[float, float, float] | tuple[float, float, float, pd.DataFrame]:
    """

    :param values: Values as array of shape (N1, N2) with NaN for masked values
    :param gsd: Ground sampling distance
    :param area: Size of integration area (squared unit of ground sampling distance)
    :param perc_min_valid: Minimum valid area in the patch
    :param patch_shape: Shape of patch, either "circular" or "square"
    :param method: Method to perform the convolution, "scipy" or "numba"
    :param statistic_between_patches: Statistic to compute between all patches, typically a measure of spread, applied
        to the first in-patch statistic, which is typically the mean
    :param verbose: Print statement to console
    :param return_in_patch_statistics: Whether to return the dataframe of statistics for all patches and areas


    :return: Statistic between patches, Number of patches, Exact discretized area, (Optional) Dataframe of per-patch
        statistics
    """

    
    
    if patch_shape.lower() == "circular":
        kernel_size = int(np.round(2 * np.sqrt(area / np.pi) / gsd, decimals=0))
    
    elif patch_shape.lower() == "square":
        kernel_size = int(np.round(np.sqrt(area) / gsd, decimals=0))

    else:
        raise ValueError('Kernel shape should be "square" or "circular".')

    if verbose:
        print("Computing the convolution on the entire array...")
    mean_img, nb_valid_img, nb_pixel_per_kernel = mean_filter_nan(
        img=values, kernel_size=kernel_size, kernel_shape=patch_shape, method=method
    )

    
    mean_img[nb_valid_img < nb_pixel_per_kernel * perc_min_valid / 100.0] = np.nan

    
    
    

    
    if verbose:
        print("Computing statistic between patches for all independent combinations...")
    list_statistic_estimates = []
    list_nb_independent_patches = []
    for i in range(kernel_size):
        for j in range(kernel_size):
            statistic = statistic_between_patches(mean_img[i::kernel_size, j::kernel_size].ravel())
            nb_patches = np.count_nonzero(np.isfinite(mean_img[i::kernel_size, j::kernel_size]))
            list_statistic_estimates.append(statistic)
            list_nb_independent_patches.append(nb_patches)

    if return_in_patch_statistics:
        
        df = pd.DataFrame(
            data={
                "nanmean": mean_img[::kernel_size, ::kernel_size].ravel(),
                "count": nb_valid_img[::kernel_size, ::kernel_size].ravel(),
            }
        )

    
    
    average_statistic = float(np.nanmean(np.asarray(list_statistic_estimates)))
    nb_independent_patches = float(np.nanmean(np.asarray(list_nb_independent_patches)))
    exact_area = nb_pixel_per_kernel * gsd**2

    if return_in_patch_statistics:
        return average_statistic, nb_independent_patches, exact_area, df
    else:
        return average_statistic, nb_independent_patches, exact_area


def _patches_loop_quadrants(
    values: NDArrayf,
    gsd: float,
    area: float,
    patch_shape: str = "circular",
    n_patches: int = 1000,
    perc_min_valid: float = 80.0,
    statistics_in_patch: Iterable[Callable[[NDArrayf], np.floating[Any]] | str] = (np.nanmean,),
    statistic_between_patches: Callable[[NDArrayf], np.floating[Any]] = nmad,
    verbose: bool = False,
    random_state: None | int | np.random.RandomState = None,
    return_in_patch_statistics: bool = False,
) -> tuple[float, float, float] | tuple[float, float, float, pd.DataFrame]:
    """
    Patches method for empirical estimation of the standard error over an integration area


    :param values: Values as array of shape (N1, N2) with NaN for masked values
    :param gsd: Ground sampling distance
    :param area: Size of integration area (squared unit of ground sampling distance)
    :param perc_min_valid: Minimum valid area in the patch
    :param statistics_in_patch: List of statistics to compute in each patch (count is computed by default; only the
    first statistic is used by statistic_between_patches)
    :param statistic_between_patches: Statistic to compute between all patches, typically a measure of spread, applied
        to the first in-patch statistic, which is typically the mean
    :param patch_shape: Shape of patch, either "circular" or "square".
    :param n_patches: Maximum number of patches to sample
    :param verbose: Print statement to console
    :param random_state: Random state or seed number to use for calculations (to fix random sampling during testing)
    :param return_in_patch_statistics: Whether to return the dataframe of statistics for all patches and areas

    :return: Statistic between patches, Number of patches, Exact discretized area, Dataframe of per-patch statistics
    """

    list_statistics_in_patch = list(statistics_in_patch)
    
    list_statistics_in_patch.append("count")

    
    statistics_name = [f if isinstance(f, str) else f.__name__ for f in list_statistics_in_patch]

    
    rnd = _random_state_definition(random_state=random_state)

    
    nx, ny = np.shape(values)

    kernel_size = int(np.round(np.sqrt(area) / gsd, decimals=0))

    
    nx_sub = int(np.floor((nx - 1) / kernel_size))
    ny_sub = int(np.floor((ny - 1) / kernel_size))
    
    rad = int(np.round(np.sqrt(area / np.pi) / gsd, decimals=0))

    
    if patch_shape.lower() == "square":
        nb_pixel_exact = nx_sub * ny_sub
        exact_area = nb_pixel_exact * gsd**2
    elif patch_shape.lower() == "circular":
        nb_pixel_exact = np.count_nonzero(_create_circular_mask(shape=(nx, ny), radius=rad))
        exact_area = nb_pixel_exact * gsd**2

    
    list_quadrant = [[i, j] for i in range(nx_sub) for j in range(ny_sub)]
    u = 0
    
    remaining_nsamp = n_patches
    list_df = []
    while len(list_quadrant) > 0 and u < n_patches:

        
        
        list_idx_quadrant = rnd.choice(len(list_quadrant), size=min(len(list_quadrant), 10 * remaining_nsamp))

        for idx_quadrant in list_idx_quadrant:

            if verbose:
                print("Working on a new quadrant")

            
            i = list_quadrant[idx_quadrant][0]
            j = list_quadrant[idx_quadrant][1]

            
            if patch_shape.lower() == "square":
                patch = values[
                    kernel_size * i : kernel_size * (i + 1), kernel_size * j : kernel_size * (j + 1)
                ].flatten()
            elif patch_shape.lower() == "circular":
                center_x = np.floor(kernel_size * (i + 1 / 2))
                center_y = np.floor(kernel_size * (j + 1 / 2))
                mask = _create_circular_mask((nx, ny), center=(center_x, center_y), radius=rad)
                patch = values[mask]
            else:
                raise ValueError("Patch method must be square or circular.")

            
            nb_pixel_total = len(patch)
            nb_pixel_valid = len(patch[np.isfinite(patch)])
            if nb_pixel_valid >= np.ceil(perc_min_valid / 100.0 * nb_pixel_total) and nb_pixel_total == nb_pixel_exact:
                u = u + 1
                if u > n_patches:
                    break
                if verbose:
                    print("Found valid quadrant " + str(u) + " (maximum: " + str(n_patches) + ")")

                df = pd.DataFrame()
                df = df.assign(tile=[str(i) + "_" + str(j)])
                for j, statistic in enumerate(list_statistics_in_patch):
                    if isinstance(statistic, str):
                        if statistic == "count":
                            df[statistic] = [nb_pixel_valid]
                        else:
                            raise ValueError('No other string than "count" are supported for named statistics.')
                    else:
                        df[statistics_name[j]] = [statistic(patch[np.isfinite(patch)].astype("float64"))]

                list_df.append(df)

        
        remaining_nsamp = n_patches - u
        
        list_quadrant = [c for j, c in enumerate(list_quadrant) if j not in list_idx_quadrant]

    if len(list_df) > 0:
        df_all = pd.concat(list_df)
        
        average_statistic = float(statistic_between_patches(df_all[statistics_name[0]].values))
        nb_independent_patches = np.count_nonzero(np.isfinite(df_all[statistics_name[0]].values))
    else:
        df_all = pd.DataFrame()
        for j, _ in enumerate(list_statistics_in_patch):
            df_all[statistics_name[j]] = [np.nan]
        average_statistic = np.nan
        nb_independent_patches = 0
        warnings.warn("No valid patch found covering this area size, returning NaN for statistic.")

    if return_in_patch_statistics:
        return average_statistic, nb_independent_patches, exact_area, df_all
    else:
        return average_statistic, nb_independent_patches, exact_area


@overload
def patches_method(
    values: NDArrayf | RasterType,
    areas: list[float],
    gsd: float = None,
    stable_mask: NDArrayf | VectorType | gpd.GeoDataFrame = None,
    unstable_mask: NDArrayf | VectorType | gpd.GeoDataFrame = None,
    statistics_in_patch: tuple[Callable[[NDArrayf], np.floating[Any]] | str] = (np.nanmean,),
    statistic_between_patches: Callable[[NDArrayf], np.floating[Any]] = nmad,
    perc_min_valid: float = 80.0,
    patch_shape: str = "circular",
    vectorized: bool = True,
    convolution_method: str = "scipy",
    n_patches: int = 1000,
    verbose: bool = False,
    *,
    return_in_patch_statistics: Literal[False] = False,
    random_state: None | int | np.random.RandomState = None,
) -> pd.DataFrame:
    ...


@overload
def patches_method(
    values: NDArrayf | RasterType,
    areas: list[float],
    gsd: float = None,
    stable_mask: NDArrayf | VectorType | gpd.GeoDataFrame = None,
    unstable_mask: NDArrayf | VectorType | gpd.GeoDataFrame = None,
    statistics_in_patch: tuple[Callable[[NDArrayf], np.floating[Any]] | str] = (np.nanmean,),
    statistic_between_patches: Callable[[NDArrayf], np.floating[Any]] = nmad,
    perc_min_valid: float = 80.0,
    patch_shape: str = "circular",
    vectorized: bool = True,
    convolution_method: str = "scipy",
    n_patches: int = 1000,
    verbose: bool = False,
    *,
    return_in_patch_statistics: Literal[True],
    random_state: None | int | np.random.RandomState = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    ...


def patches_method(
    values: NDArrayf | RasterType,
    areas: list[float],
    gsd: float = None,
    stable_mask: NDArrayf | VectorType | gpd.GeoDataFrame = None,
    unstable_mask: NDArrayf | VectorType | gpd.GeoDataFrame = None,
    statistics_in_patch: tuple[Callable[[NDArrayf], np.floating[Any]] | str] = (np.nanmean,),
    statistic_between_patches: Callable[[NDArrayf], np.floating[Any]] = nmad,
    perc_min_valid: float = 80.0,
    patch_shape: str = "circular",
    vectorized: bool = True,
    convolution_method: str = "scipy",
    n_patches: int = 1000,
    verbose: bool = False,
    return_in_patch_statistics: bool = False,
    random_state: None | int | np.random.RandomState = None,
) -> pd.DataFrame | tuple[pd.DataFrame, pd.DataFrame]:

    """
    Monte Carlo patches method that samples multiple patches of terrain, square or circular, of a certain area and
    computes a statistic in each patch. Then, another statistic is computed between all patches. Typically, a statistic
    of central tendency (e.g., the mean) is computed for each patch, then a statistic of spread (e.g., the NMAD) is
    computed on the central tendency of all the patches. This specific procedure gives an empirical estimate of the
    standard error of the mean.

    The function returns the exact areas of the patches, which might differ from the input due to rasterization of the
    shapes.

    By default, the fast vectorized method based on a convolution of all pixels is used, but only works with the mean.
    To compute other statistics (possibly a list), the non-vectorized method that randomly samples quadrants of the
    input array up to a certain number of patches "n_patches" can be used.

    The per-patch statistics can be returned as a concatenated dataframe using the "return_in_patch_statistics"
    argument, not done by default due to large sizes.

    :param values: Values as array or Raster
    :param areas: List of patch areas to process (squared unit of ground sampling distance; exact patch areas might not
        always match these accurately due to rasterization, and are returned as outputs)
    :param gsd: Ground sampling distance
    :param stable_mask: Vector shapefile of stable terrain (if values is Raster), or boolean array of same shape as
        values
    :param unstable_mask: Vector shapefile of unstable terrain (if values is Raster), or boolean array of same shape
        as values
    :param statistics_in_patch: List of statistics to compute in each patch (count is computed by default;
        only mean and count supported for vectorized version)
    :param statistic_between_patches: Statistic to compute between all patches, typically a measure of spread, applied
        to the first in-patch statistic, which is typically the mean
    :param perc_min_valid: Minimum valid area in the patch
    :param patch_shape: Shape of patch, either "circular" or "square"
    :param vectorized: Whether to use the vectorized (convolution) method or the for loop in quadrants
    :param convolution_method: Convolution method to use, either "scipy" or "numba" (only for vectorized)
    :param n_patches: Maximum number of patches to sample (only for non-vectorized)
    :param verbose: Print statement to console
    :param return_in_patch_statistics: Whether to return the dataframe of statistics for all patches and areas
    :param random_state: Random state or seed number to use for calculations (only for non-vectorized, for testing)

    :return: Dataframe of statistic between patches with independent patches count and exact areas,
        (Optional) Dataframe of per-patch statistics
    """

    
    values_arr, gsd = _preprocess_values_with_mask_to_array(
        values=values, include_mask=stable_mask, exclude_mask=unstable_mask, gsd=gsd
    )

    
    list_stats = []
    list_nb_patches = []
    list_exact_areas = []

    
    if return_in_patch_statistics:
        list_df = []

    
    for area in areas:
        
        if vectorized:
            outputs = _patches_convolution(
                values=values_arr,
                gsd=gsd,
                area=area,
                perc_min_valid=perc_min_valid,
                patch_shape=patch_shape,
                method=convolution_method,
                statistic_between_patches=statistic_between_patches,
                verbose=verbose,
                return_in_patch_statistics=return_in_patch_statistics,
            )

        
        else:
            outputs = _patches_loop_quadrants(
                values=values_arr,
                gsd=gsd,
                area=area,
                patch_shape=patch_shape,
                n_patches=n_patches,
                perc_min_valid=perc_min_valid,
                statistics_in_patch=statistics_in_patch,
                statistic_between_patches=statistic_between_patches,
                verbose=verbose,
                return_in_patch_statistics=return_in_patch_statistics,
                random_state=random_state,
            )

        list_stats.append(outputs[0])
        list_nb_patches.append(outputs[1])
        list_exact_areas.append(outputs[2])
        if return_in_patch_statistics:
            
            
            df: pd.DataFrame = outputs[3]  
            df["areas"] = area
            df["exact_areas"] = outputs[2]
            list_df.append(df)

    
    df_statistic = pd.DataFrame(
        data={
            statistic_between_patches.__name__: list_stats,
            "nb_indep_patches": list_nb_patches,
            "exact_areas": list_exact_areas,
            "areas": areas,
        }
    )

    if return_in_patch_statistics:
        
        df_tot = pd.concat(list_df)
        return df_statistic, df_tot
    else:
        return df_statistic


def plot_variogram(
    df: pd.DataFrame,
    list_fit_fun: list[Callable[[NDArrayf], NDArrayf]] = None,
    list_fit_fun_label: list[str] = None,
    ax: matplotlib.axes.Axes = None,
    xscale: str = "linear",
    xscale_range_split: list[float] = None,
    xlabel: str = None,
    ylabel: str = None,
    xlim: str = None,
    ylim: str = None,
) -> None:
    """
    Plot empirical variogram, and optionally also plot one or several model fits.
    Input dataframe is expected to be the output of xdem.spatialstats.sample_empirical_variogram.
    Input function model is expected to be the output of xdem.spatialstats.fit_sum_model_variogram.

    :param df: Empirical variogram, formatted as a dataframe with count (pairwise sample count), lags
        (upper bound of spatial lag bin), exp (experimental variance), and err_exp (error on experimental variance)
    :param list_fit_fun: List of model function fits
    :param list_fit_fun_label: List of model function fits labels
    :param ax: Plotting ax to use, creates a new one by default
    :param xscale: Scale of X-axis
    :param xscale_range_split: List of ranges at which to split the figure
    :param xlabel: Label of X-axis
    :param ylabel: Label of Y-axis
    :param xlim: Limits of X-axis
    :param ylim: Limits of Y-axis
    :return:
    """

    
    if ax is None:
        fig = plt.figure()
        ax = plt.subplot(111)
    elif isinstance(ax, matplotlib.axes.Axes):
        fig = ax.figure
    else:
        raise ValueError("ax must be a matplotlib.axes.Axes instance or None")

    
    expected_values = ["exp", "lags", "count"]
    for val in expected_values:
        if val not in df.columns.values:
            raise ValueError(f'The expected variable "{val}" is not part of the provided dataframe column names.')

    
    ax.axis("off")

    if ylabel is None:
        ylabel = r"Variance [$\mu$ $\pm \sigma$]"
    if xlabel is None:
        xlabel = "Spatial lag (m)"

    init_gridsize = [10, 10]
    
    
    if xscale_range_split is None:
        nb_subpanels = 1
        if xscale == "log":
            xmin = [np.min(df.lags) / 2]
        else:
            xmin = [0]
        xmax = [np.max(df.lags)]
        xgridmin = [0]
        xgridmax = [init_gridsize[0]]
        gridsize = init_gridsize
    
    else:
        
        if xscale_range_split[0] != 0:
            if xscale == "log":
                first_xmin = np.min(df.lags) / 2
            else:
                first_xmin = 0
            xscale_range_split = [first_xmin] + xscale_range_split
        
        if xscale_range_split[-1] != np.max(df.lags):
            xscale_range_split.append(np.max(df.lags))

        
        nb_subpanels = len(xscale_range_split) - 1
        gridsize = init_gridsize.copy()
        gridsize[0] *= nb_subpanels
        
        xmin = []
        xmax = []
        xgridmin = []
        xgridmax = []
        for i in range(nb_subpanels):
            xmin.append(xscale_range_split[i])
            xmax.append(xscale_range_split[i + 1])
            xgridmin.append(init_gridsize[0] * i)
            xgridmax.append(init_gridsize[0] * (i + 1))

    
    grid = plt.GridSpec(gridsize[1], gridsize[0], wspace=0.5, hspace=0.5)

    
    for k in range(nb_subpanels):
        
        ax0 = ax.inset_axes(grid[:3, xgridmin[k] : xgridmax[k]].get_position(fig).bounds)
        ax0.set_xscale(xscale)
        ax0.set_xticks([])

        
        interval_var = [0] + list(df.lags)
        for i in range(len(df)):
            count = df["count"].values[i]
            ax0.fill_between(
                [interval_var[i], interval_var[i + 1]],
                [0] * 2,
                [count] * 2,
                facecolor=plt.cm.Greys(0.75),
                alpha=1,
                edgecolor="white",
                linewidth=0.5,
            )
        if k == 0:
            ax0.set_ylabel("Sample count")
            
            ax0.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
        else:
            ax0.set_yticks([])
        
        ax0.set_xlim((xmin[k], xmax[k]))

        
        ax1 = ax.inset_axes(grid[3:, xgridmin[k] : xgridmax[k]].get_position(fig).bounds)

        
        bins_center = np.subtract(df.lags, np.diff([0] + df.lags.tolist()) / 2)

        
        if np.all(np.isnan(df.err_exp)):
            ax1.scatter(bins_center, df.exp, label="Empirical variogram", color="blue", marker="x")
        
        else:
            ax1.errorbar(bins_center, df.exp, yerr=df.err_exp, label="Empirical variogram (1-sigma std error)", fmt="x")

        
        if list_fit_fun is not None:
            for i, fit_fun in enumerate(list_fit_fun):
                x = np.linspace(xmin[k], xmax[k], 1000)
                y = fit_fun(x)

                if list_fit_fun_label is not None:
                    ax1.plot(x, y, linestyle="dashed", label=list_fit_fun_label[i], zorder=30)
                else:
                    ax1.plot(x, y, linestyle="dashed", color="black", zorder=30)

            if list_fit_fun_label is None:
                ax1.plot([], [], linestyle="dashed", color="black", label="Model fit")

        ax1.set_xscale(xscale)
        if nb_subpanels > 1 and k == (nb_subpanels - 1):
            ax1.xaxis.set_ticks(np.linspace(xmin[k], xmax[k], 3))
        elif nb_subpanels > 1:
            ax1.xaxis.set_ticks(np.linspace(xmin[k], xmax[k], 3)[:-1])

        if xlim is None:
            ax1.set_xlim((xmin[k], xmax[k]))
        else:
            ax1.set_xlim(xlim)

        if ylim is not None:
            ax1.set_ylim(ylim)
        else:
            if np.all(np.isnan(df.err_exp)):
                ax1.set_ylim((0, 1.05 * np.nanmax(df.exp)))
            else:
                ax1.set_ylim((0, np.nanmax(df.exp) + np.nanmean(df.err_exp)))

        if k == int(nb_subpanels / 2):
            ax1.set_xlabel(xlabel)
        if k == nb_subpanels - 1:
            ax1.legend(loc="lower right")
        if k == 0:
            ax1.set_ylabel(ylabel)
        else:
            ax1.set_yticks([])


def plot_1d_binning(
    df: pd.DataFrame,
    var_name: str,
    statistic_name: str,
    label_var: str | None = None,
    label_statistic: str | None = None,
    min_count: int = 30,
    ax: matplotlib.axes.Axes | None = None,
) -> None:
    """
    Plot a statistic and its count along a single binning variable.
    Input is expected to be formatted as the output of the xdem.spatialstats.nd_binning function.

    :param df: Output dataframe of nd_binning
    :param var_name: Name of binning variable to plot
    :param statistic_name: Name of statistic of interest to plot
    :param label_var: Label of binning variable
    :param label_statistic: Label of statistic of interest
    :param min_count: Removes statistic values computed with a count inferior to this minimum value
    :param ax: Plotting ax to use, creates a new one by default
    """

    
    if ax is None:
        fig = plt.figure()
        ax = plt.subplot(111)
    elif isinstance(ax, matplotlib.axes.Axes):
        fig = ax.figure
    else:
        raise ValueError("ax must be a matplotlib.axes.Axes instance or None.")

    if var_name not in df.columns.values:
        raise ValueError(f'The variable "{var_name}" is not part of the provided dataframe column names.')

    if statistic_name not in df.columns.values:
        raise ValueError(f'The statistic "{statistic_name}" is not part of the provided dataframe column names.')

    
    ax.axis("off")

    if label_var is None:
        label_var = var_name
    if label_statistic is None:
        label_statistic = statistic_name

    
    df_sub = df[np.logical_and(df.nd == 1, np.isfinite(pd.IntervalIndex(df[var_name]).mid))].copy()
    
    df_sub.loc[df_sub["count"] < min_count, statistic_name] = np.nan

    
    grid = plt.GridSpec(10, 10, wspace=0.5, hspace=0.5)

    
    ax0 = ax.inset_axes(grid[:3, :].get_position(fig).bounds)
    ax0.set_xticks([])

    
    interval_var = pd.IntervalIndex(df_sub[var_name])
    for i in range(len(df_sub)):
        count = df_sub["count"].values[i]
        ax0.fill_between(
            [interval_var[i].left, interval_var[i].right],
            [0] * 2,
            [count] * 2,
            facecolor=plt.cm.Greys(0.75),
            alpha=1,
            edgecolor="white",
            linewidth=0.5,
        )
    ax0.set_ylabel("Sample count")
    
    ax0.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))

    
    
    if np.sum(~(np.abs(df_sub["count"].values[0] - df_sub["count"].values) < 5)) <= 2:
        ax0.text(
            0.5,
            0.5,
            "Fixed number of\n samples: " + "{:,}".format(int(df_sub["count"].values[0])),
            ha="center",
            va="center",
            fontweight="bold",
            transform=ax0.transAxes,
            bbox=dict(facecolor="white", alpha=0.8),
        )

    ax0.set_ylim((0, 1.1 * np.max(df_sub["count"].values)))
    ax0.set_xlim((np.min(interval_var.left), np.max(interval_var.right)))

    
    ax1 = ax.inset_axes(grid[3:, :].get_position(fig).bounds)
    ax1.scatter(interval_var.mid, df_sub[statistic_name], marker="x")
    ax1.set_xlabel(label_var)
    ax1.set_ylabel(label_statistic)
    ax1.set_xlim((np.min(interval_var.left), np.max(interval_var.right)))


def plot_2d_binning(
    df: pd.DataFrame,
    var_name_1: str,
    var_name_2: str,
    statistic_name: str,
    label_var_name_1: str | None = None,
    label_var_name_2: str | None = None,
    label_statistic: str | None = None,
    cmap: matplotlib.colors.Colormap = plt.cm.Reds,
    min_count: int = 30,
    scale_var_1: str = "linear",
    scale_var_2: str = "linear",
    vmin: np.floating[Any] = None,
    vmax: np.floating[Any] = None,
    nodata_color: str | tuple[float, float, float, float] = "yellow",
    ax: matplotlib.axes.Axes | None = None,
) -> None:
    """
    Plot one statistic and its count along two binning variables.
    Input is expected to be formatted as the output of the xdem.spatialstats.nd_binning function.

    :param df: Output dataframe of nd_binning
    :param var_name_1: Name of first binning variable to plot
    :param var_name_2: Name of second binning variable to plot
    :param statistic_name: Name of statistic of interest to plot
    :param label_var_name_1: Label of first binning variable
    :param label_var_name_2: Label of second binning variable
    :param label_statistic: Label of statistic of interest
    :param cmap: Colormap
    :param min_count: Removes statistic values computed with a count inferior to this minimum value
    :param scale_var_1: Scale along the axis of the first variable
    :param scale_var_2: Scale along the axis of the second variable
    :param vmin: Minimum statistic value in colormap range
    :param vmax: Maximum statistic value in colormap range
    :param nodata_color: Color for no data bins
    :param ax: Plotting ax to use, creates a new one by default
    """

    
    if ax is None:
        fig = plt.figure(figsize=(8, 6))
        ax = plt.subplot(111)
    elif isinstance(ax, matplotlib.axes.Axes):
        fig = ax.figure
    else:
        raise ValueError("ax must be a matplotlib.axes.Axes instance or None.")

    if var_name_1 not in df.columns.values:
        raise ValueError(f'The variable "{var_name_1}" is not part of the provided dataframe column names.')
    elif var_name_2 not in df.columns.values:
        raise ValueError(f'The variable "{var_name_2}" is not part of the provided dataframe column names.')

    if statistic_name not in df.columns.values:
        raise ValueError(f'The statistic "{statistic_name}" is not part of the provided dataframe column names.')

    
    ax.axis("off")

    
    df_sub = df[
        np.logical_and.reduce(
            (
                df.nd == 2,
                np.isfinite(pd.IntervalIndex(df[var_name_1]).mid),
                np.isfinite(pd.IntervalIndex(df[var_name_2]).mid),
            )
        )
    ].copy()
    
    df_sub.loc[df_sub["count"] < min_count, statistic_name] = np.nan

    
    
    
    

    
    grid = plt.GridSpec(10, 10, wspace=0.5, hspace=0.5)

    
    ax0 = ax.inset_axes(grid[:3, :-3].get_position(fig).bounds)
    ax0.set_xscale(scale_var_1)
    ax0.set_xticklabels([])

    
    interval_var_1 = pd.IntervalIndex(df_sub[var_name_1])
    df_sub["var1_mid"] = interval_var_1.mid.values
    unique_var_1 = np.unique(df_sub.var1_mid)
    list_counts = []
    for i in range(len(unique_var_1)):
        df_var1 = df_sub[df_sub.var1_mid == unique_var_1[i]]
        count = np.nansum(df_var1["count"].values)
        list_counts.append(count)
        ax0.fill_between(
            [df_var1[var_name_1].values[0].left, df_var1[var_name_1].values[0].right],
            [0] * 2,
            [count] * 2,
            facecolor=plt.cm.Greys(0.75),
            alpha=1,
            edgecolor="white",
            linewidth=0.5,
        )
    ax0.set_ylabel("Sample count")
    
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        ax0.set_ylim((0, 1.1 * np.max(list_counts)))
        ax0.set_xlim((np.min(interval_var_1.left), np.max(interval_var_1.right)))
    ax0.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
    ax0.spines["top"].set_visible(False)
    ax0.spines["right"].set_visible(False)
    
    if np.sum(~(np.abs(list_counts[0] - np.array(list_counts)) < 5)) <= 2:
        ax0.text(
            0.5,
            0.5,
            "Fixed number of\nsamples: " + f"{int(list_counts[0]):,}",
            ha="center",
            va="center",
            fontweight="bold",
            transform=ax0.transAxes,
            bbox=dict(facecolor="white", alpha=0.8),
        )

    
    ax1 = ax.inset_axes(grid[3:, -3:].get_position(fig).bounds)
    ax1.set_yscale(scale_var_2)
    ax1.set_yticklabels([])

    
    interval_var_2 = pd.IntervalIndex(df_sub[var_name_2])
    df_sub["var2_mid"] = interval_var_2.mid.values
    unique_var_2 = np.unique(df_sub.var2_mid)
    list_counts = []
    for i in range(len(unique_var_2)):
        df_var2 = df_sub[df_sub.var2_mid == unique_var_2[i]]
        count = np.nansum(df_var2["count"].values)
        list_counts.append(count)
        ax1.fill_between(
            [0, count],
            [df_var2[var_name_2].values[0].left] * 2,
            [df_var2[var_name_2].values[0].right] * 2,
            facecolor=plt.cm.Greys(0.75),
            alpha=1,
            edgecolor="white",
            linewidth=0.5,
        )
    ax1.set_xlabel("Sample count")
    
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        ax1.set_xlim((0, 1.1 * np.max(list_counts)))
        ax1.set_ylim((np.min(interval_var_2.left), np.max(interval_var_2.right)))
    ax1.ticklabel_format(axis="x", style="sci", scilimits=(0, 0))
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    
    if np.sum(~(np.abs(list_counts[0] - np.array(list_counts)) < 5)) <= 2:
        ax1.text(
            0.5,
            0.5,
            "Fixed number of\nsamples: " + f"{int(list_counts[0]):,}",
            ha="center",
            va="center",
            fontweight="bold",
            transform=ax1.transAxes,
            rotation=90,
            bbox=dict(facecolor="white", alpha=0.8),
        )

    
    ax2 = ax.inset_axes(grid[3:, :-3].get_position(fig).bounds)

    
    if vmin is None and vmax is None:
        vmax = np.nanpercentile(df_sub[statistic_name].values, 99)
        vmin = np.nanpercentile(df_sub[statistic_name].values, 1)

    
    col_bounds = np.array([vmin, np.mean(np.asarray([vmin, vmax])), vmax])
    cb = []
    cb_val = np.linspace(0, 1, len(col_bounds))
    for j in range(len(cb_val)):
        cb.append(cmap(cb_val[j]))
    cmap_cus = colors.LinearSegmentedColormap.from_list(
        "my_cb", list(zip((col_bounds - min(col_bounds)) / (max(col_bounds - min(col_bounds))), cb)), N=1000
    )

    
    for i in range(len(unique_var_1)):
        for j in range(len(unique_var_2)):
            df_both = df_sub[np.logical_and(df_sub.var1_mid == unique_var_1[i], df_sub.var2_mid == unique_var_2[j])]

            stat = df_both[statistic_name].values[0]
            if np.isfinite(stat):
                stat_col = max(0.0001, min(0.9999, (stat - min(col_bounds)) / (max(col_bounds) - min(col_bounds))))
                col = cmap_cus(stat_col)
            else:
                col = nodata_color

            ax2.fill_between(
                [df_both[var_name_1].values[0].left, df_both[var_name_1].values[0].right],
                [df_both[var_name_2].values[0].left] * 2,
                [df_both[var_name_2].values[0].right] * 2,
                facecolor=col,
                alpha=1,
                edgecolor="white",
            )

    ax2.set_xlabel(label_var_name_1)
    ax2.set_ylabel(label_var_name_2)
    ax2.set_xscale(scale_var_1)
    ax2.set_yscale(scale_var_2)
    
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        ax2.set_xlim((np.min(interval_var_1.left), np.max(interval_var_1.right)))
        ax2.set_ylim((np.min(interval_var_2.left), np.max(interval_var_2.right)))

    
    axcmap = ax.inset_axes(grid[:3, -3:].get_position(fig).bounds)

    
    axcmap.set_xticks([])
    axcmap.set_yticks([])
    axcmap.spines["top"].set_visible(False)
    axcmap.spines["left"].set_visible(False)
    axcmap.spines["right"].set_visible(False)
    axcmap.spines["bottom"].set_visible(False)

    
    cbaxes = axcmap.inset_axes([0, 0.75, 1, 0.2], label="cmap")

    
    norm = colors.Normalize(vmin=min(col_bounds), vmax=max(col_bounds))
    sm = plt.cm.ScalarMappable(cmap=cmap_cus, norm=norm)
    sm.set_array([])
    cb = plt.colorbar(sm, cax=cbaxes, orientation="horizontal", extend="both", shrink=0.8)
    cb.ax.tick_params(width=0.5, length=2)
    cb.set_label(label_statistic)

    
    nodata = axcmap.inset_axes([0.4, 0.1, 0.2, 0.2], label="nodata")

    
    nodata.fill_between([0, 1], [0, 0], [1, 1], facecolor=nodata_color)
    nodata.set_xlim((0, 1))
    nodata.set_ylim((0, 1))
    nodata.set_xticks([])
    nodata.set_yticks([])
    nodata.text(0.5, -0.25, "No data", ha="center", va="top")
