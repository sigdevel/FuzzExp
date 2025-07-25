"""DEM coregistration classes and functions."""
from __future__ import annotations

import concurrent.futures
import copy
import warnings
from typing import Any, Callable, Generator, TypedDict, TypeVar, overload

try:
    import cv2

    _has_cv2 = True
except ImportError:
    _has_cv2 = False
import fiona
import geoutils as gu
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import rasterio as rio
import rasterio.warp  
import rasterio.windows  
import scipy
import scipy.interpolate
import scipy.ndimage
import scipy.optimize
import skimage.transform
from geoutils import spatial_tools
from geoutils._typing import AnyNumber
from geoutils.georaster import RasterType
from rasterio import Affine
from tqdm import tqdm, trange

import xdem
from xdem._typing import MArrayf, NDArrayf

try:
    import pytransform3d.transformations
    from pytransform3d.transform_manager import TransformManager

    _HAS_P3D = True
except ImportError:
    _HAS_P3D = False


def filter_by_range(ds: rio.DatasetReader, rangelim: tuple[float, float]) -> MArrayf:
    """
    Function to filter values using a range.
    """
    print("Excluding values outside of range: {:f} to {:f}".format(*rangelim))
    out = np.ma.masked_outside(ds, *rangelim)
    out.set_fill_value(ds.fill_value)
    return out


def filtered_slope(ds_slope: rio.DatasetReader, slope_lim: tuple[float, float] = (0.1, 40)) -> MArrayf:
    print("Slope filter: %0.2f - %0.2f" % slope_lim)
    print("Initial count: %i" % ds_slope.count())
    flt_slope = filter_by_range(ds_slope, slope_lim)
    print(flt_slope.count())
    return flt_slope


def apply_xy_shift(ds: rio.DatasetReader, dx: float, dy: float) -> NDArrayf:
    """
    Apply horizontal shift to rio dataset using Transform affine matrix
    :param ds: DEM
    :param dx: dx shift value
    :param dy: dy shift value

    Returns:
    Rio Dataset with updated transform
    """
    print("X shift: ", dx)
    print("Y shift: ", dy)

    
    gt_orig = ds.transform
    gt_align = Affine(gt_orig.a, gt_orig.b, gt_orig.c + dx, gt_orig.d, gt_orig.e, gt_orig.f + dy)

    print("Original transform:", gt_orig)
    print("Updated transform:", gt_align)

    
    ds_align = ds
    meta_update = ds.meta.copy()
    meta_update({"driver": "GTiff", "height": ds.shape[1], "width": ds.shape[2], "transform": gt_align, "crs": ds.crs})
    
    with rasterio.open(ds_align, "w", **meta_update) as dest:
        dest.write(ds_align)

    return ds_align


def apply_z_shift(ds: rio.DatasetReader, dz: float) -> float:
    """
    Apply vertical shift to rio dataset using Transform affine matrix
    :param ds: DEM
    :param dz: dz shift value
    """
    src_dem = rio.open(ds)
    a = src_dem.read(1)
    ds_shift = a + dz
    return ds_shift


def get_horizontal_shift(
    elevation_difference: NDArrayf, slope: NDArrayf, aspect: NDArrayf, min_count: int = 20
) -> tuple[float, float, float]:
    """
    Calculate the horizontal shift between two DEMs using the method presented in Nuth and Kääb (2011).

    :param elevation_difference: The elevation difference (reference_dem - aligned_dem).
    :param slope: A slope map with the same shape as elevation_difference (units = pixels?).
    :param aspect: An aspect map with the same shape as elevation_difference (units = radians).
    :param min_count: The minimum allowed bin size to consider valid.

    :raises ValueError: If very few finite values exist to analyse.

    :returns: The pixel offsets in easting, northing, and the c_parameter (altitude?).
    """
    input_x_values = aspect

    with np.errstate(divide="ignore", invalid="ignore"):
        input_y_values = elevation_difference / slope

    
    x_values = input_x_values[np.isfinite(input_x_values) & np.isfinite(input_y_values)]
    y_values = input_y_values[np.isfinite(input_x_values) & np.isfinite(input_y_values)]

    assert y_values.shape[0] > 0

    
    lower_percentile = np.percentile(y_values, 1)
    upper_percentile = np.percentile(y_values, 99)
    valids = np.where((y_values > lower_percentile) & (y_values < upper_percentile) & (np.abs(y_values) < 200))
    x_values = x_values[valids]
    y_values = y_values[valids]

    
    step = np.pi / 36
    slice_bounds = np.arange(start=0, stop=2 * np.pi, step=step)
    y_medians = np.zeros([len(slice_bounds)])
    count = y_medians.copy()
    for i, bound in enumerate(slice_bounds):
        y_slice = y_values[(bound < x_values) & (x_values < (bound + step))]
        if y_slice.shape[0] > 0:
            y_medians[i] = np.median(y_slice)
        count[i] = y_slice.shape[0]

    
    y_medians = y_medians[count > min_count]
    slice_bounds = slice_bounds[count > min_count]

    if slice_bounds.shape[0] < 10:
        raise ValueError("Less than 10 different cells exist.")

    
    initial_guess: tuple[float, float, float] = (3 * np.std(y_medians) / (2**0.5), 0.0, np.mean(y_medians))

    def estimate_ys(x_values: NDArrayf, parameters: tuple[float, float, float]) -> NDArrayf:
        """
        Estimate y-values from x-values and the current parameters.

        y(x) = a * cos(b - x) + c

        :param x_values: The x-values to feed the above function.
        :param parameters: The a, b, and c parameters to feed the above function

        :returns: Estimated y-values with the same shape as the given x-values
        """
        return parameters[0] * np.cos(parameters[1] - x_values) + parameters[2]

    def residuals(parameters: tuple[float, float, float], y_values: NDArrayf, x_values: NDArrayf) -> NDArrayf:
        """
        Get the residuals between the estimated and measured values using the given parameters.

        err(x, y) = est_y(x) - y

        :param parameters: The a, b, and c parameters to use for the estimation.
        :param y_values: The measured y-values.
        :param x_values: The measured x-values

        :returns: An array of residuals with the same shape as the input arrays.
        """
        err = estimate_ys(x_values, parameters) - y_values
        return err

    
    results = scipy.optimize.least_squares(
        fun=residuals, x0=initial_guess, args=(y_medians, slice_bounds), xtol=1e-8, gtol=None, ftol=None
    )

    
    a_parameter, b_parameter, c_parameter = results.x
    a_parameter = np.round(a_parameter, 2)
    b_parameter = np.round(b_parameter, 2)

    
    east_offset = a_parameter * np.sin(b_parameter)
    north_offset = a_parameter * np.cos(b_parameter)

    return east_offset, north_offset, c_parameter


def calculate_slope_and_aspect(dem: NDArrayf) -> tuple[NDArrayf, NDArrayf]:
    """
    Calculate the slope and aspect of a DEM.

    :param dem: A numpy array of elevation values.

    :returns:  The slope (in pixels??) and aspect (in radians) of the DEM.
    """
    
    

    
    gradient_y, gradient_x = np.gradient(dem)

    slope_px = np.sqrt(gradient_x**2 + gradient_y**2)
    aspect = np.arctan2(-gradient_x, gradient_y)
    aspect += np.pi

    return slope_px, aspect


def deramping(
    elevation_difference: NDArrayf,
    x_coordinates: NDArrayf,
    y_coordinates: NDArrayf,
    degree: int,
    verbose: bool = False,
    metadata: dict[str, Any] | None = None,
) -> Callable[[NDArrayf, NDArrayf], NDArrayf]:
    """
    Calculate a deramping function to account for rotational and non-rigid components of the elevation difference.

    :param elevation_difference: The elevation difference array to analyse.
    :param x_coordinates: x-coordinates of the above array (must have the same shape as elevation_difference)
    :param y_coordinates: y-coordinates of the above array (must have the same shape as elevation_difference)
    :param degree: The polynomial degree to estimate the ramp.
    :param verbose: Print the least squares optimization progress.
    :param metadata: Optional. A metadata dictionary that will be updated with the key "deramp".

    :returns: A callable function to estimate the ramp.
    """
    "This function is deprecated in favour of the new Coreg class.", DeprecationWarning)
    
    valid_diffs = elevation_difference[np.isfinite(elevation_difference)]
    valid_x_coords = x_coordinates[np.isfinite(elevation_difference)]
    valid_y_coords = y_coordinates[np.isfinite(elevation_difference)]

    
    if valid_x_coords.shape[0] > 500_000:
        random_indices = np.random.randint(0, valid_x_coords.shape[0] - 1, 500_000)
        valid_diffs = valid_diffs[random_indices]
        valid_x_coords = valid_x_coords[random_indices]
        valid_y_coords = valid_y_coords[random_indices]

    
    def estimate_values(
        x_coordinates: NDArrayf, y_coordinates: NDArrayf, coefficients: NDArrayf, degree: int
    ) -> NDArrayf:
        """
        Estimate values from a 2D-polynomial.

        :param x_coordinates: x-coordinates of the difference array (must have the same shape as elevation_difference).
        :param y_coordinates: y-coordinates of the difference array (must have the same shape as elevation_difference).
        :param coefficients: The coefficients (a, b, c, etc.) of the polynomial.
        :param degree: The degree of the polynomial.

        :raises ValueError: If the length of the coefficients list is not compatible with the degree.

        :returns: The values estimated by the polynomial.
        """
        
        coefficient_size = (degree + 1) * (degree + 2) / 2
        if len(coefficients) != coefficient_size:
            raise ValueError()

        
        estimated_values = np.sum(
            [
                coefficients[k * (k + 1) // 2 + j] * x_coordinates ** (k - j) * y_coordinates**j
                for k in range(degree + 1)
                for j in range(k + 1)
            ],
            axis=0,
        )
        return estimated_values  

    
    def residuals(
        coefficients: NDArrayf, values: NDArrayf, x_coordinates: NDArrayf, y_coordinates: NDArrayf, degree: int
    ) -> NDArrayf:
        """
        Calculate the difference between the estimated and measured values.

        :param coefficients: Coefficients for the estimation.
        :param values: The measured values.
        :param x_coordinates: The x-coordinates of the values.
        :param y_coordinates: The y-coordinates of the values.
        :param degree: The degree of the polynomial to estimate.

        :returns: An array of residuals.
        """
        error = estimate_values(x_coordinates, y_coordinates, coefficients, degree) - values
        error = error[np.isfinite(error)]

        return error

    
    
    initial_guess = np.zeros(shape=((degree + 1) * (degree + 2) // 2))
    if verbose:
        print("Deramping...")
    coefficients = scipy.optimize.least_squares(
        fun=residuals,
        x0=initial_guess,
        args=(valid_diffs, valid_x_coords, valid_y_coords, degree),
        verbose=2 if verbose and degree > 1 else 0,
    ).x

    

    def ramp(x_coordinates: NDArrayf, y_coordinates: NDArrayf) -> NDArrayf:
        """
        Get the values of the ramp that corresponds to given coordinates.

        :param x_coordinates: x-coordinates of interest.
        :param y_coordinates: y-coordinates of interest.

        :returns: The estimated ramp offsets.
        """
        return estimate_values(x_coordinates, y_coordinates, coefficients, degree)

    if metadata is not None:
        metadata["deramp"] = {
            "coefficients": coefficients,
            "nmad": xdem.spatialstats.nmad(
                residuals(coefficients, valid_diffs, valid_x_coords, valid_y_coords, degree)
            ),
        }

    
    return ramp


def mask_as_array(
    reference_raster: gu.georaster.Raster, mask: str | gu.geovector.Vector | gu.georaster.Raster
) -> NDArrayf:
    """
    Convert a given mask into an array.

    :param reference_raster: The raster to use for rasterizing the mask if the mask is a vector.
    :param mask: A valid Vector, Raster or a respective filepath to a mask.

    :raises: ValueError: If the mask path is invalid.
    :raises: TypeError: If the wrong mask type was given.

    :returns: The mask as a squeezed array.
    """
    
    if isinstance(mask, str):
        
        try:
            mask = gu.geovector.Vector(mask)
        
        except fiona.errors.DriverError:
            try:
                mask = gu.georaster.Raster(mask)
            
            except rio.errors.RasterioIOError:
                raise ValueError(f"Mask path not in a supported Raster or Vector format: {mask}")

    
    
    if isinstance(mask, gu.geovector.Vector):
        mask_array = mask.create_mask(reference_raster)
    elif isinstance(mask, gu.georaster.Raster):
        
        true_value = np.nanmax(mask.data) if not np.nanmax(mask.data) in [0, False] else True
        mask_array = (mask.data == true_value).squeeze()
    else:
        raise TypeError(
            f"Mask has invalid type: {type(mask)}. Expected one of: "
            f"{[gu.georaster.Raster, gu.geovector.Vector, str, type(None)]}"
        )

    return mask_array


def _transform_to_bounds_and_res(
    shape: tuple[int, ...], transform: rio.transform.Affine
) -> tuple[rio.coords.BoundingBox, float]:
    """Get the bounding box and (horizontal) resolution from a transform and the shape of a DEM."""
    bounds = rio.coords.BoundingBox(*rio.transform.array_bounds(shape[0], shape[1], transform=transform))
    resolution = (bounds.right - bounds.left) / shape[1]

    return bounds, resolution


def _get_x_and_y_coords(shape: tuple[int, ...], transform: rio.transform.Affine) -> tuple[NDArrayf, NDArrayf]:
    """Generate center coordinates from a transform and the shape of a DEM."""
    bounds, resolution = _transform_to_bounds_and_res(shape, transform)
    x_coords, y_coords = np.meshgrid(
        np.linspace(bounds.left + resolution / 2, bounds.right - resolution / 2, num=shape[1]),
        np.linspace(bounds.bottom + resolution / 2, bounds.top - resolution / 2, num=shape[0])[::-1],
    )
    return x_coords, y_coords


CoregType = TypeVar("CoregType", bound="Coreg")


class CoregDict(TypedDict, total=False):
    """
    Defining the type of each possible key in the metadata dictionary of Coreg classes.
    The parameter total=False means that the key are not required. In the recent PEP 655 (
    https://peps.python.org/pep-0655/) there is an easy way to specific Required or NotRequired for each key, if we
    want to change this in the future.
    """

    bias_func: Callable[[NDArrayf], np.floating[Any]]
    func: Callable[[NDArrayf, NDArrayf], NDArrayf]
    bias: np.floating[Any] | float | np.integer[Any] | int
    matrix: NDArrayf
    centroid: tuple[float, float, float]
    offset_east_px: float
    offset_north_px: float
    coefficients: NDArrayf
    coreg_meta: list[Any]
    resolution: float
    
    pipeline: list[Any]


class Coreg:
    """
    Generic Coreg class.

    Made to be subclassed.
    """

    _fit_called: bool = False  
    _is_affine: bool | None = None

    def __init__(self, meta: CoregDict | None = None, matrix: NDArrayf | None = None) -> None:
        """Instantiate a generic Coreg method."""
        self._meta: CoregDict = meta or {}  

        if matrix is not None:
            with warnings.catch_warnings():
                
                warnings.filterwarnings("ignore", message="`np.float` is a deprecated alias for the builtin `float`")
                valid_matrix = pytransform3d.transformations.check_transform(matrix)
            self._meta["matrix"] = valid_matrix

    def fit(
        self: CoregType,
        reference_dem: NDArrayf | MArrayf | RasterType,
        dem_to_be_aligned: NDArrayf | MArrayf | RasterType,
        inlier_mask: NDArrayf | None = None,
        transform: rio.transform.Affine | None = None,
        weights: NDArrayf | None = None,
        subsample: float | int = 1.0,
        verbose: bool = False,
        random_state: None | np.random.RandomState | np.random.Generator | int = None,
    ) -> CoregType:
        """
        Estimate the coregistration transform on the given DEMs.

        :param reference_dem: 2D array of elevation values acting reference.
        :param dem_to_be_aligned: 2D array of elevation values to be aligned.
        :param inlier_mask: Optional. 2D boolean array of areas to include in the analysis (inliers=True).
        :param transform: Optional. Transform of the reference_dem. Mandatory in some cases.
        :param weights: Optional. Per-pixel weights for the coregistration.
        :param subsample: Subsample the input to increase performance. <1 is parsed as a fraction. >1 is a pixel count.
        :param verbose: Print progress messages to stdout.
        :param random_state: Random state or seed number to use for calculations (to fix random sampling during testing)
        """

        if weights is not None:
            raise NotImplementedError("Weights have not yet been implemented")

        
        if not all(isinstance(dem, (np.ndarray, gu.Raster)) for dem in (reference_dem, dem_to_be_aligned)):
            raise ValueError(
                "Both DEMs need to be array-like (implement a numpy array interface)."
                f"'reference_dem': {reference_dem}, 'dem_to_be_aligned': {dem_to_be_aligned}"
            )

        
        if isinstance(dem_to_be_aligned, gu.Raster) and isinstance(reference_dem, gu.Raster):
            dem_to_be_aligned = dem_to_be_aligned.reproject(reference_dem, silent=True).data

        
        
        
        for name, dem in [("reference_dem", reference_dem), ("dem_to_be_aligned", dem_to_be_aligned)]:
            if isinstance(dem, gu.Raster):
                if transform is None:
                    transform = dem.transform
                elif transform is not None:
                    warnings.warn(f"'{name}' of type {type(dem)} overrides the given 'transform'")

                """
                if name == "reference_dem":
                    reference_dem = dem.data
                else:
                    dem_to_be_aligned = dem.data
                """

        if transform is None:
            raise ValueError("'transform' must be given if both DEMs are array-like.")

        ref_dem, ref_mask = spatial_tools.get_array_and_mask(reference_dem)
        tba_dem, tba_mask = spatial_tools.get_array_and_mask(dem_to_be_aligned)

        
        if inlier_mask is not None:
            inlier_mask = np.asarray(inlier_mask).squeeze()
            assert inlier_mask.dtype == bool, f"Invalid mask dtype: '{inlier_mask.dtype}'. Expected 'bool'"

            if np.all(~inlier_mask):
                raise ValueError("'inlier_mask' had no inliers.")

            ref_dem[~inlier_mask] = np.nan
            tba_dem[~inlier_mask] = np.nan

        if np.all(ref_mask):
            raise ValueError("'reference_dem' had only NaNs")
        if np.all(tba_mask):
            raise ValueError("'dem_to_be_aligned' had only NaNs")

        
        if subsample != 1.0:
            
            full_mask = (
                ~ref_mask & ~tba_mask & (np.asarray(inlier_mask) if inlier_mask is not None else True)
            ).squeeze()
            
            if subsample < 1.0:
                subsample = int(np.count_nonzero(full_mask) * (1 - subsample))

            
            random_falses = np.random.choice(np.argwhere(full_mask.flatten()).squeeze(), int(subsample), replace=False)
            
            cols = (random_falses // full_mask.shape[0]).astype(int)
            rows = random_falses % full_mask.shape[0]
            
            full_mask[rows, cols] = False

        
        self._fit_func(ref_dem=ref_dem, tba_dem=tba_dem, transform=transform, weights=weights, verbose=verbose)

        
        self._fit_called = True

        return self

    @overload
    def apply(self, dem: MArrayf, transform: rio.transform.Affine | None = None, **kwargs: Any) -> MArrayf:
        ...

    @overload
    def apply(self, dem: NDArrayf, transform: rio.transform.Affine | None = None, **kwargs: Any) -> NDArrayf:
        ...

    @overload
    def apply(self, dem: RasterType, transform: rio.transform.Affine | None = None, **kwargs: Any) -> RasterType:
        ...

    def apply(
        self, dem: RasterType | NDArrayf | MArrayf, transform: rio.transform.Affine | None = None, **kwargs: Any
    ) -> RasterType | NDArrayf | MArrayf:
        """
        Apply the estimated transform to a DEM.

        :param dem: A DEM array or Raster to apply the transform on.
        :param transform: The transform object of the DEM. Required if 'dem' is an array and not a Raster.
        :param kwargs: Any optional arguments to be passed to either self._apply_func or apply_matrix.

        :returns: The transformed DEM.
        """
        if not self._fit_called and self._meta.get("matrix") is None:
            raise AssertionError(".fit() does not seem to have been called yet")

        if isinstance(dem, gu.Raster):
            if transform is None:
                transform = dem.transform
            else:
                warnings.warn(f"DEM of type {type(dem)} overrides the given 'transform'")
        else:
            if transform is None:
                raise ValueError("'transform' must be given if DEM is array-like.")

        
        dem_array, dem_mask = spatial_tools.get_array_and_mask(dem)

        if np.all(dem_mask):
            raise ValueError("'dem' had only NaNs")

        
        try:
            
            applied_dem = self._apply_func(dem_array, transform, **kwargs)  
        
        except NotImplementedError:
            if self.is_affine:  
                
                if "dilate_mask" in kwargs.keys():
                    dilate_mask = kwargs["dilate_mask"]
                    kwargs.pop("dilate_mask")
                else:
                    dilate_mask = True

                
                applied_dem = apply_matrix(
                    dem_array,
                    transform=transform,
                    matrix=self.to_matrix(),
                    centroid=self._meta.get("centroid"),
                    dilate_mask=dilate_mask,
                    **kwargs,
                )
            else:
                raise ValueError("Coreg method is non-rigid but has no implemented _apply_func")

        
        applied_dem = applied_dem.astype("float32")

        
        final_mask = ~np.isfinite(applied_dem)

        
        if isinstance(dem, (np.ma.masked_array, gu.Raster)):
            applied_dem = np.ma.masked_array(applied_dem, mask=final_mask)  
        else:
            applied_dem[final_mask] = np.nan

        
        if isinstance(dem, gu.Raster):
            return dem.copy(new_array=applied_dem)
            

        return applied_dem

    def apply_pts(self, coords: NDArrayf) -> NDArrayf:
        """
        Apply the estimated transform to a set of 3D points.

        :param coords: A (N, 3) array of X/Y/Z coordinates or one coordinate of shape (3,).

        :returns: The transformed coordinates.
        """
        if not self._fit_called and self._meta.get("matrix") is None:
            raise AssertionError(".fit() does not seem to have been called yet")
        
        if np.shape(coords) == (3,):
            coords = np.reshape(coords, (1, 3))

        assert (
            len(np.shape(coords)) == 2 and np.shape(coords)[1] == 3
        ), f"'coords' shape must be (N, 3). Given shape: {np.shape(coords)}"

        coords_c = coords.copy()

        
        try:
            transformed_points = self._apply_pts_func(coords)
        
        except NotImplementedError:
            if self.is_affine:  
                
                if self._meta.get("centroid") is not None:
                    coords_c -= self._meta["centroid"]
                transformed_points = cv2.perspectiveTransform(coords_c.reshape(1, -1, 3), self.to_matrix()).squeeze()
                if self._meta.get("centroid") is not None:
                    transformed_points += self._meta["centroid"]

            else:
                raise ValueError("Coreg method is non-rigid but has not implemented _apply_pts_func")

        return transformed_points

    @property
    def is_affine(self) -> bool:
        """Check if the transform be explained by a 3D affine transform."""
        
        
        if self._is_affine is None:
            try:  
                self.to_matrix()
                self._is_affine = True
            except (ValueError, NotImplementedError):
                self._is_affine = False

        return self._is_affine

    def to_matrix(self) -> NDArrayf:
        """Convert the transform to a 4x4 transformation matrix."""
        return self._to_matrix_func()

    def centroid(self) -> tuple[float, float, float] | None:
        """Get the centroid of the coregistration, if defined."""
        meta_centroid = self._meta.get("centroid")

        if meta_centroid is None:
            return None

        
        return meta_centroid[0], meta_centroid[1], meta_centroid[2]

    def residuals(
        self,
        reference_dem: NDArrayf,
        dem_to_be_aligned: NDArrayf,
        inlier_mask: NDArrayf | None = None,
        transform: rio.transform.Affine | None = None,
    ) -> NDArrayf:
        """
        Calculate the residual offsets (the difference) between two DEMs after applying the transformation.

        :param reference_dem: 2D array of elevation values acting reference.
        :param dem_to_be_aligned: 2D array of elevation values to be aligned.
        :param inlier_mask: Optional. 2D boolean array of areas to include in the analysis (inliers=True).
        :param transform: Optional. Transform of the reference_dem. Mandatory in some cases.

        :returns: A 1D array of finite residuals.
        """
        
        aligned_dem = self.apply(dem_to_be_aligned, transform=transform)

        
        ref_arr, ref_mask = spatial_tools.get_array_and_mask(reference_dem)

        if inlier_mask is None:
            inlier_mask = np.ones(ref_arr.shape, dtype=bool)

        
        full_mask = (~ref_mask) & np.isfinite(aligned_dem) & inlier_mask

        
        diff = ref_arr - aligned_dem

        
        if "float" in str(diff.dtype):
            full_mask[(diff == np.finfo(diff.dtype).min) | np.isinf(diff)] = False

        
        return diff[full_mask]

    @overload
    def error(
        self,
        reference_dem: NDArrayf,
        dem_to_be_aligned: NDArrayf,
        error_type: list[str],
        inlier_mask: NDArrayf | None = None,
        transform: rio.transform.Affine | None = None,
    ) -> list[np.floating[Any] | float | np.integer[Any] | int]:
        ...

    @overload
    def error(
        self,
        reference_dem: NDArrayf,
        dem_to_be_aligned: NDArrayf,
        error_type: str = "nmad",
        inlier_mask: NDArrayf | None = None,
        transform: rio.transform.Affine | None = None,
    ) -> np.floating[Any] | float | np.integer[Any] | int:
        ...

    def error(
        self,
        reference_dem: NDArrayf,
        dem_to_be_aligned: NDArrayf,
        error_type: str | list[str] = "nmad",
        inlier_mask: NDArrayf | None = None,
        transform: rio.transform.Affine | None = None,
    ) -> np.floating[Any] | float | np.integer[Any] | int | list[np.floating[Any] | float | np.integer[Any] | int]:
        """
        Calculate the error of a coregistration approach.

        Choices:
            - "nmad": Default. The Normalized Median Absolute Deviation of the residuals.
            - "median": The median of the residuals.
            - "mean": The mean/average of the residuals
            - "std": The standard deviation of the residuals.
            - "rms": The root mean square of the residuals.
            - "mae": The mean absolute error of the residuals.
            - "count": The residual count.

        :param reference_dem: 2D array of elevation values acting reference.
        :param dem_to_be_aligned: 2D array of elevation values to be aligned.
        :param error_type: The type of error measure to calculate. May be a list of error types.
        :param inlier_mask: Optional. 2D boolean array of areas to include in the analysis (inliers=True).
        :param transform: Optional. Transform of the reference_dem. Mandatory in some cases.

        :returns: The error measure of choice for the residuals.
        """
        if isinstance(error_type, str):
            error_type = [error_type]

        residuals = self.residuals(
            reference_dem=reference_dem,
            dem_to_be_aligned=dem_to_be_aligned,
            inlier_mask=inlier_mask,
            transform=transform,
        )

        def rms(res: NDArrayf) -> np.floating[Any]:
            return np.sqrt(np.mean(np.square(res)))

        def mae(res: NDArrayf) -> np.floating[Any]:
            return np.mean(np.abs(res))

        def count(res: NDArrayf) -> int:
            return res.size

        error_functions: dict[str, Callable[[NDArrayf], np.floating[Any] | float | np.integer[Any] | int]] = {
            "nmad": xdem.spatialstats.nmad,
            "median": np.median,
            "mean": np.mean,
            "std": np.std,
            "rms": rms,
            "mae": mae,
            "count": count,
        }

        try:
            errors = [error_functions[err_type](residuals) for err_type in error_type]
        except KeyError as exception:
            raise ValueError(
                f"Invalid 'error_type'{'s' if len(error_type) > 1 else ''}: "
                f"'{error_type}'. Choices: {list(error_functions.keys())}"
            ) from exception

        return errors if len(errors) > 1 else errors[0]

    @classmethod
    def from_matrix(cls, matrix: NDArrayf) -> Coreg:
        """
        Instantiate a generic Coreg class from a transformation matrix.

        :param matrix: A 4x4 transformation matrix. Shape must be (4,4).

        :raises ValueError: If the matrix is incorrectly formatted.

        :returns: The instantiated generic Coreg class.
        """
        if np.any(~np.isfinite(matrix)):
            raise ValueError(f"Matrix has non-finite values:\n{matrix}")
        with warnings.catch_warnings():
            
            warnings.filterwarnings("ignore", message="`np.float` is a deprecated alias for the builtin `float`")
            valid_matrix = pytransform3d.transformations.check_transform(matrix)
        return cls(matrix=valid_matrix)

    @classmethod
    def from_translation(cls, x_off: float = 0.0, y_off: float = 0.0, z_off: float = 0.0) -> Coreg:
        """
        Instantiate a generic Coreg class from a X/Y/Z translation.

        :param x_off: The offset to apply in the X (west-east) direction.
        :param y_off: The offset to apply in the Y (south-north) direction.
        :param z_off: The offset to apply in the Z (vertical) direction.

        :raises ValueError: If the given translation contained invalid values.

        :returns: An instantiated generic Coreg class.
        """
        matrix = np.diag(np.ones(4, dtype=float))
        matrix[0, 3] = x_off
        matrix[1, 3] = y_off
        matrix[2, 3] = z_off

        return cls.from_matrix(matrix)

    def copy(self: CoregType) -> CoregType:
        """Return an identical copy of the class."""
        new_coreg = self.__new__(type(self))

        new_coreg.__dict__ = {key: copy.copy(value) for key, value in self.__dict__.items()}

        return new_coreg

    def __add__(self, other: Coreg) -> CoregPipeline:
        """Return a pipeline consisting of self and the other coreg function."""
        if not isinstance(other, Coreg):
            raise ValueError(f"Incompatible add type: {type(other)}. Expected 'Coreg' subclass")
        return CoregPipeline([self, other])

    def _fit_func(
        self,
        ref_dem: NDArrayf,
        tba_dem: NDArrayf,
        transform: rio.transform.Affine | None,
        weights: NDArrayf | None,
        verbose: bool = False,
    ) -> None:
        
        raise NotImplementedError("This should have been implemented by subclassing")

    def _to_matrix_func(self) -> NDArrayf:
        

        
        meta_matrix = self._meta.get("matrix")
        if meta_matrix is not None:
            assert meta_matrix.shape == (4, 4), f"Invalid _meta matrix shape. Expected: (4, 4), got {meta_matrix.shape}"
            return meta_matrix

        raise NotImplementedError("This should be implemented by subclassing")

    def _apply_func(self, dem: NDArrayf, transform: rio.transform.Affine, **kwargs: Any) -> NDArrayf:
        
        raise NotImplementedError("This should have been implemented by subclassing")

    def _apply_pts_func(self, coords: NDArrayf) -> NDArrayf:
        
        raise NotImplementedError("This should have been implemented by subclassing")


class BiasCorr(Coreg):
    """
    DEM bias correction.

    Estimates the mean (or median, weighted avg., etc.) offset between two DEMs.
    """

    def __init__(self, bias_func: Callable[[NDArrayf], np.floating[Any]] = np.average) -> None:  
        
        """
        Instantiate a bias correction object.

        :param bias_func: The function to use for calculating the bias. Default: (weighted) average.
        """
        self._meta: CoregDict = {}  

        super().__init__(meta={"bias_func": bias_func})

    def _fit_func(
        self,
        ref_dem: NDArrayf,
        tba_dem: NDArrayf,
        transform: rio.transform.Affine | None,
        weights: NDArrayf | None,
        verbose: bool = False,
    ) -> None:
        """Estimate the bias using the bias_func."""
        if verbose:
            print("Estimating bias...")
        diff = ref_dem - tba_dem
        diff = diff[np.isfinite(diff)]

        if np.count_nonzero(np.isfinite(diff)) == 0:
            raise ValueError("No finite values in bias comparison.")

        
        bias = (
            self._meta["bias_func"](diff) if weights is None else self._meta["bias_func"](diff, weights)  
        )
        
        

        if verbose:
            print("Bias estimated")

        self._meta["bias"] = bias

    def _to_matrix_func(self) -> NDArrayf:
        """Convert the bias to a transform matrix."""
        empty_matrix = np.diag(np.ones(4, dtype=float))

        empty_matrix[2, 3] += self._meta["bias"]

        return empty_matrix


class ICP(Coreg):
    """
    Iterative Closest Point DEM coregistration.
    Based on 3D registration of Besl and McKay (1992), https://doi.org/10.1117/12.57955.

    Estimates a rigid transform (rotation + translation) between two DEMs.

    Requires 'opencv'
    See opencv docs for more info: https://docs.opencv.org/master/dc/d9b/classcv_1_1ppf__match__3d_1_1ICP.html
    """

    def __init__(
        self, max_iterations: int = 100, tolerance: float = 0.05, rejection_scale: float = 2.5, num_levels: int = 6
    ) -> None:
        """
        Instantiate an ICP coregistration object.

        :param max_iterations: The maximum allowed iterations before stopping.
        :param tolerance: The residual change threshold after which to stop the iterations.
        :param rejection_scale: The threshold (std * rejection_scale) to consider points as outliers.
        :param num_levels: Number of octree levels to consider. A higher number is faster but may be more inaccurate.
        """
        if not _has_cv2:
            raise ValueError("Optional dependency needed. Install 'opencv'")
        self.max_iterations = max_iterations
        self.tolerance = tolerance
        self.rejection_scale = rejection_scale
        self.num_levels = num_levels

        super().__init__()

    def _fit_func(
        self,
        ref_dem: NDArrayf,
        tba_dem: NDArrayf,
        transform: rio.transform.Affine | None,
        weights: NDArrayf | None,
        verbose: bool = False,
    ) -> None:
        """Estimate the rigid transform from tba_dem to ref_dem."""

        if weights is not None:
            warnings.warn("ICP was given weights, but does not support it.")

        bounds, resolution = _transform_to_bounds_and_res(ref_dem.shape, transform)
        points: dict[str, NDArrayf] = {}
        
        x_coords, y_coords = _get_x_and_y_coords(ref_dem.shape, transform)

        centroid = (np.mean([bounds.left, bounds.right]), np.mean([bounds.bottom, bounds.top]), 0.0)
        
        x_coords -= centroid[0]
        y_coords -= centroid[1]
        for key, dem in zip(["ref", "tba"], [ref_dem, tba_dem]):

            gradient_x, gradient_y = np.gradient(dem)

            normal_east = np.sin(np.arctan(gradient_y / resolution)) * -1
            normal_north = np.sin(np.arctan(gradient_x / resolution))
            normal_up = 1 - np.linalg.norm([normal_east, normal_north], axis=0)

            valid_mask = ~np.isnan(dem) & ~np.isnan(normal_east) & ~np.isnan(normal_north)

            point_cloud = np.dstack(
                [
                    x_coords[valid_mask],
                    y_coords[valid_mask],
                    dem[valid_mask],
                    normal_east[valid_mask],
                    normal_north[valid_mask],
                    normal_up[valid_mask],
                ]
            ).squeeze()

            points[key] = point_cloud[~np.any(np.isnan(point_cloud), axis=1)].astype("float32")

            icp = cv2.ppf_match_3d_ICP(self.max_iterations, self.tolerance, self.rejection_scale, self.num_levels)
        if verbose:
            print("Running ICP...")
        try:
            _, residual, matrix = icp.registerModelToScene(points["tba"], points["ref"])
        except cv2.error as exception:
            if "(expected: 'n > 0'), where" not in str(exception):
                raise exception

            raise ValueError(
                "Not enough valid points in input data."
                f"'reference_dem' had {points['ref'].size} valid points."
                f"'dem_to_be_aligned' had {points['tba'].size} valid points."
            )

        if verbose:
            print("ICP finished")

        assert residual < 1000, f"ICP coregistration failed: residual={residual}, threshold: 1000"

        self._meta["centroid"] = centroid
        self._meta["matrix"] = matrix


class Deramp(Coreg):
    """
    Polynomial DEM deramping.

    Estimates an n-D polynomial between the difference of two DEMs.
    """

    def __init__(self, degree: int = 1, subsample: int | float = 5e5) -> None:
        """
        Instantiate a deramping correction object.

        :param degree: The polynomial degree to estimate. degree=0 is a simple bias correction.
        :param subsample: Factor for subsampling the input raster for speed-up.
            If <= 1, will be considered a fraction of valid pixels to extract.
            If > 1 will be considered the number of pixels to extract.

        """
        self.degree = degree
        self.subsample = subsample

        super().__init__()

    def _fit_func(
        self,
        ref_dem: NDArrayf,
        tba_dem: NDArrayf,
        transform: rio.transform.Affine | None,
        weights: NDArrayf | None,
        verbose: bool = False,
    ) -> None:
        """Fit the dDEM between the DEMs to a least squares polynomial equation."""
        x_coords, y_coords = _get_x_and_y_coords(ref_dem.shape, transform)

        ddem = ref_dem - tba_dem
        valid_mask = np.isfinite(ddem)
        ddem = ddem[valid_mask]
        x_coords = x_coords[valid_mask]
        y_coords = y_coords[valid_mask]

        
        def poly2d(x_coordinates: NDArrayf, y_coordinates: NDArrayf, coefficients: NDArrayf) -> NDArrayf:
            """
            Estimate values from a 2D-polynomial.

            :param x_coordinates: x-coordinates of the difference array (must have the same shape as
                elevation_difference).
            :param y_coordinates: y-coordinates of the difference array (must have the same shape as
                elevation_difference).
            :param coefficients: The coefficients (a, b, c, etc.) of the polynomial.
            :param degree: The degree of the polynomial.

            :raises ValueError: If the length of the coefficients list is not compatible with the degree.

            :returns: The values estimated by the polynomial.
            """
            
            coefficient_size = (self.degree + 1) * (self.degree + 2) / 2
            if len(coefficients) != coefficient_size:
                raise ValueError()

            
            estimated_values = np.sum(
                [
                    coefficients[k * (k + 1) // 2 + j] * x_coordinates ** (k - j) * y_coordinates**j
                    for k in range(self.degree + 1)
                    for j in range(k + 1)
                ],
                axis=0,
            )
            return estimated_values  

        def residuals(coefs: NDArrayf, x_coords: NDArrayf, y_coords: NDArrayf, targets: NDArrayf) -> NDArrayf:
            res = targets - poly2d(x_coords, y_coords, coefs)
            return res[np.isfinite(res)]

        if verbose:
            print("Estimating deramp function...")

        
        
        max_points = np.size(x_coords)
        if (self.subsample <= 1) & (self.subsample >= 0):
            npoints = int(self.subsample * max_points)
        elif self.subsample > 1:
            npoints = int(self.subsample)
        else:
            raise ValueError("`subsample` must be >= 0")

        if max_points > npoints:
            indices = np.random.choice(max_points, npoints, replace=False)
            x_coords = x_coords[indices]
            y_coords = y_coords[indices]
            ddem = ddem[indices]

        
        coefs = scipy.optimize.leastsq(
            func=residuals,
            x0=np.zeros(shape=((self.degree + 1) * (self.degree + 2) // 2)),
            args=(x_coords, y_coords, ddem),
        )

        def fit_func(x: NDArrayf, y: NDArrayf) -> NDArrayf:
            return poly2d(x, y, coefs[0])

        self._meta["coefficients"] = coefs[0]
        self._meta["func"] = fit_func

    def _apply_func(self, dem: NDArrayf, transform: rio.transform.Affine, **kwargs: Any) -> NDArrayf:
        """Apply the deramp function to a DEM."""
        x_coords, y_coords = _get_x_and_y_coords(dem.shape, transform)

        ramp = self._meta["func"](x_coords, y_coords)

        return dem + ramp

    def _apply_pts_func(self, coords: NDArrayf) -> NDArrayf:
        """Apply the deramp function to a set of points."""
        new_coords = coords.copy()

        new_coords[:, 2] += self._meta["func"](new_coords[:, 0], new_coords[:, 1])

        return new_coords

    def _to_matrix_func(self) -> NDArrayf:
        """Return a transform matrix if possible."""
        if self.degree > 1:
            raise ValueError(
                "Nonlinear deramping degrees cannot be represented as transformation matrices."
                f" (max 1, given: {self.degree})"
            )
        if self.degree == 1:
            raise NotImplementedError("Vertical shift, rotation and horizontal scaling has to be implemented.")

        
        empty_matrix = np.diag(np.ones(4, dtype=float))

        empty_matrix[2, 3] += self._meta["coefficients"][0]

        return empty_matrix


class CoregPipeline(Coreg):
    """
    A sequential set of coregistration steps.
    """

    def __init__(self, pipeline: list[Coreg]) -> None:
        """
        Instantiate a new coregistration pipeline.

        :param: Coregistration steps to run in the sequence they are given.
        """
        self.pipeline = pipeline

        super().__init__()

    def __repr__(self) -> str:
        return f"CoregPipeline: {self.pipeline}"

    def copy(self: CoregType) -> CoregType:
        """Return an identical copy of the class."""
        new_coreg = self.__new__(type(self))

        new_coreg.__dict__ = {key: copy.copy(value) for key, value in self.__dict__.items() if key != "pipeline"}
        new_coreg.pipeline = [step.copy() for step in self.pipeline]

        return new_coreg

    def _fit_func(
        self,
        ref_dem: NDArrayf,
        tba_dem: NDArrayf,
        transform: rio.transform.Affine | None,
        weights: NDArrayf | None,
        verbose: bool = False,
    ) -> None:
        """Fit each coregistration step with the previously transformed DEM."""
        tba_dem_mod = tba_dem.copy()

        for i, coreg in enumerate(self.pipeline):
            if verbose:
                print(f"Running pipeline step: {i + 1} / {len(self.pipeline)}")
            coreg._fit_func(ref_dem, tba_dem_mod, transform=transform, weights=weights, verbose=verbose)
            coreg._fit_called = True

            tba_dem_mod = coreg.apply(tba_dem_mod, transform)

    def _apply_func(self, dem: NDArrayf, transform: rio.transform.Affine, **kwargs: Any) -> NDArrayf:
        """Apply the coregistration steps sequentially to a DEM."""
        dem_mod = dem.copy()
        for coreg in self.pipeline:
            dem_mod = coreg.apply(dem_mod, transform, **kwargs)

        return dem_mod

    def _apply_pts_func(self, coords: NDArrayf) -> NDArrayf:
        """Apply the coregistration steps sequentially to a set of points."""
        coords_mod = coords.copy()

        for coreg in self.pipeline:
            coords_mod = coreg.apply_pts(coords_mod).reshape(coords_mod.shape)

        return coords_mod

    def _to_matrix_func(self) -> NDArrayf:
        """Try to join the coregistration steps to a single transformation matrix."""
        if not _HAS_P3D:
            raise ValueError("Optional dependency needed. Install 'pytransform3d'")

        transform_mgr = TransformManager()

        with warnings.catch_warnings():
            
            warnings.filterwarnings("ignore", message="`np.float` is a deprecated alias for the builtin `float`")
            for i, coreg in enumerate(self.pipeline):
                new_matrix = coreg.to_matrix()

                transform_mgr.add_transform(i, i + 1, new_matrix)

            return transform_mgr.get_transform(0, len(self.pipeline))

    def __iter__(self) -> Generator[Coreg, None, None]:
        """Iterate over the pipeline steps."""
        yield from self.pipeline

    def __add__(self, other: list[Coreg] | Coreg | CoregPipeline) -> CoregPipeline:
        """Append Coreg(s) or a CoregPipeline to the pipeline."""
        if not isinstance(other, Coreg):
            other = list(other)
        else:
            other = [other]

        pipelines = self.pipeline + other

        return CoregPipeline(pipelines)


class NuthKaab(Coreg):
    """
    Nuth and Kääb (2011) DEM coregistration.

    Implemented after the paper:
    https://doi.org/10.5194/tc-5-271-2011
    """

    def __init__(self, max_iterations: int = 10, offset_threshold: float = 0.05) -> None:
        """
        Instantiate a new Nuth and Kääb (2011) coregistration object.

        :param max_iterations: The maximum allowed iterations before stopping.
        :param offset_threshold: The residual offset threshold after which to stop the iterations.
        """
        self._meta: CoregDict
        self.max_iterations = max_iterations
        self.offset_threshold = offset_threshold

        super().__init__()

    def _fit_func(
        self,
        ref_dem: NDArrayf,
        tba_dem: NDArrayf,
        transform: rio.transform.Affine | None,
        weights: NDArrayf | None,
        verbose: bool = False,
    ) -> None:
        """Estimate the x/y/z offset between two DEMs."""
        if verbose:
            print("Running Nuth and Kääb (2011) coregistration")

        bounds, resolution = _transform_to_bounds_and_res(ref_dem.shape, transform)
        
        aligned_dem = tba_dem.copy()

        
        if verbose:
            print("   Calculate slope and aspect")
        slope, aspect = calculate_slope_and_aspect(ref_dem)

        
        east_grid = np.arange(ref_dem.shape[1])
        north_grid = np.arange(ref_dem.shape[0])

        
        elevation_function = scipy.interpolate.RectBivariateSpline(
            x=north_grid, y=east_grid, z=np.where(np.isnan(aligned_dem), -9999, aligned_dem), kx=1, ky=1
        )

        
        
        nodata_function = scipy.interpolate.RectBivariateSpline(
            x=north_grid, y=east_grid, z=np.isnan(aligned_dem), kx=1, ky=1
        )

        
        offset_east, offset_north = 0.0, 0.0

        
        elevation_difference = ref_dem - aligned_dem
        bias = np.nanmedian(elevation_difference)
        nmad_old = xdem.spatialstats.nmad(elevation_difference)
        if verbose:
            print("   Statistics on initial dh:")
            print(f"      Median = {bias:.2f} - NMAD = {nmad_old:.2f}")

        
        if verbose:
            print("   Iteratively estimating horizontal shit:")

        
        pbar = trange(self.max_iterations, disable=not verbose, desc="   Progress")
        for i in pbar:

            
            elevation_difference = ref_dem - aligned_dem
            bias = np.nanmedian(elevation_difference)
            
            elevation_difference -= bias

            
            east_diff, north_diff, _ = get_horizontal_shift(  
                elevation_difference=elevation_difference, slope=slope, aspect=aspect
            )
            if verbose:
                pbar.write(f"      ")

            
            offset_east += east_diff
            offset_north += north_diff

            
            new_elevation = elevation_function(y=east_grid + offset_east, x=north_grid - offset_north)

            
            new_nans = nodata_function(y=east_grid + offset_east, x=north_grid - offset_north)
            new_elevation[new_nans > 0] = np.nan

            
            aligned_dem = new_elevation

            
            elevation_difference = ref_dem - aligned_dem
            bias = np.nanmedian(elevation_difference)
            nmad_new = xdem.spatialstats.nmad(elevation_difference)
            nmad_gain = (nmad_new - nmad_old) / nmad_old * 100

            if verbose:
                pbar.write(f"      Median = {bias:.2f} - NMAD = {nmad_new:.2f}  ==>  Gain = {nmad_gain:.2f}%")

            
            assert ~np.isnan(nmad_new), (offset_east, offset_north)

            offset = np.sqrt(east_diff**2 + north_diff**2)
            if i > 1 and offset < self.offset_threshold:
                if verbose:
                    pbar.write(
                        f"   Last offset was below the residual offset threshold of {self.offset_threshold} -> stopping"
                    )
                break

            nmad_old = nmad_new

        
        if verbose:
            print(f"\n   Final offset in pixels (east, north) : ({offset_east:f}, {offset_north:f})")
            print("   Statistics on coregistered dh:")
            print(f"      Median = {bias:.2f} - NMAD = {nmad_new:.2f}")

        self._meta["offset_east_px"] = offset_east
        self._meta["offset_north_px"] = offset_north
        self._meta["bias"] = bias
        self._meta["resolution"] = resolution

    def _to_matrix_func(self) -> NDArrayf:
        """Return a transformation matrix from the estimated offsets."""
        offset_east = self._meta["offset_east_px"] * self._meta["resolution"]
        offset_north = self._meta["offset_north_px"] * self._meta["resolution"]

        matrix = np.diag(np.ones(4, dtype=float))
        matrix[0, 3] += offset_east
        matrix[1, 3] += offset_north
        matrix[2, 3] += self._meta["bias"]

        return matrix


def invert_matrix(matrix: NDArrayf) -> NDArrayf:
    """Invert a transformation matrix."""
    with warnings.catch_warnings():
        
        warnings.filterwarnings("ignore", message="`np.float` is a deprecated alias for the builtin `float`")

        checked_matrix = pytransform3d.transformations.check_matrix(matrix)
        
        return pytransform3d.transformations.invert_transform(checked_matrix)


def apply_matrix(
    dem: NDArrayf,
    transform: rio.transform.Affine,
    matrix: NDArrayf,
    invert: bool = False,
    centroid: tuple[float, float, float] | None = None,
    resampling: int | str = "bilinear",
    dilate_mask: bool = False,
    fill_max_search: int = 0,
) -> NDArrayf:
    """
    Apply a 3D transformation matrix to a 2.5D DEM.

    The transformation is applied as a value correction using linear deramping, and 2D image warping.

    1. Convert the DEM into a point cloud (not for gridding; for estimating the DEM shifts).
    2. Transform the point cloud in 3D using the 4x4 matrix.
    3. Measure the difference in elevation between the original and transformed points.
    4. Estimate a linear deramp from the elevation difference, and apply the correction to the DEM values.
    5. Convert the horizontal coordinates of the transformed points to pixel index coordinates.
    6. Apply the pixel-wise displacement in 2D using the new pixel coordinates.
    7. Apply the same displacement to a nodata-mask to exclude previous and/or new nans.

    :param dem: The DEM to transform.
    :param transform: The Affine transform object (georeferencing) of the DEM.
    :param matrix: A 4x4 transformation matrix to apply to the DEM.
    :param invert: Invert the transformation matrix.
    :param centroid: The X/Y/Z transformation centroid. Irrelevant for pure translations. Defaults to the midpoint (Z=0)
    :param resampling: The resampling method to use. Can be `nearest`, `bilinear`, `cubic` or an integer from 0-5.
    :param dilate_mask: DEPRECATED - This option does not do anything anymore. Will be removed in the future.
    :param fill_max_search: Set to > 0 value to fill the DEM before applying the transformation, to avoid spreading\
    gaps. The DEM will be filled with rasterio.fill.fillnodata with max_search_distance set to fill_max_search.\
    This is experimental, use at your own risk !

    :returns: The transformed DEM with NaNs as nodata values (replaces a potential mask of the input `dem`).
    """
    
    if isinstance(resampling, (int, np.integer)):
        resampling_order = resampling
    elif resampling == "cubic":
        resampling_order = 3
    elif resampling == "bilinear":
        resampling_order = 1
    elif resampling == "nearest":
        resampling_order = 0
    else:
        raise ValueError(
            f"`{resampling}` is not a valid resampling mode."
            " Choices: [`nearest`, `bilinear`, `cubic`] or an integer."
        )
    
    demc = np.array(dem)

    
    empty_matrix = np.diag(np.ones(4, float))
    empty_matrix[2, 3] = matrix[2, 3]
    if np.mean(np.abs(empty_matrix - matrix)) == 0.0:
        return demc + matrix[2, 3]

    
    if not _has_cv2:
        raise ValueError("Optional dependency needed. Install 'opencv'")

    nan_mask = spatial_tools.get_mask(dem)
    assert np.count_nonzero(~nan_mask) > 0, "Given DEM had all nans."
    
    if fill_max_search > 0:
        filled_dem = rio.fill.fillnodata(demc, mask=(~nan_mask).astype("uint8"), max_search_distance=fill_max_search)
    else:
        filled_dem = demc  

    
    x_coords, y_coords = _get_x_and_y_coords(demc.shape, transform)

    bounds, resolution = _transform_to_bounds_and_res(dem.shape, transform)

    
    if centroid is None:
        centroid = (np.mean([bounds.left, bounds.right]), np.mean([bounds.bottom, bounds.top]), 0.0)
    else:
        assert len(centroid) == 3, f"Expected centroid to be 3D X/Y/Z coordinate. Got shape of {len(centroid)}"

    
    x_coords -= centroid[0]
    y_coords -= centroid[1]

    
    point_cloud = np.dstack((x_coords, y_coords, filled_dem))

    
    point_cloud[:, 2] -= centroid[2]

    if invert:
        matrix = invert_matrix(matrix)

    
    transformed_points = cv2.perspectiveTransform(
        point_cloud.reshape((1, -1, 3)),
        matrix,
    ).reshape(point_cloud.shape)

    
    deramp = deramping(
        (point_cloud[:, :, 2] - transformed_points[:, :, 2])[~nan_mask].flatten(),
        point_cloud[:, :, 0][~nan_mask].flatten(),
        point_cloud[:, :, 1][~nan_mask].flatten(),
        degree=1,
    )
    
    filled_dem -= deramp(x_coords, y_coords)

    
    x_inds = transformed_points[:, :, 0].copy()
    x_inds[x_inds == 0] = np.nan
    y_inds = transformed_points[:, :, 1].copy()
    y_inds[y_inds == 0] = np.nan

    
    x_inds /= resolution
    y_inds /= resolution
    
    x_inds -= x_coords.min() / resolution
    
    y_inds = (y_coords.max() / resolution) - y_inds

    
    inds = np.vstack((y_inds.reshape((1,) + y_inds.shape), x_inds.reshape((1,) + x_inds.shape)))

    with warnings.catch_warnings():
        
        warnings.filterwarnings("ignore", message="Passing `np.nan` to mean no clipping in np.clip")
        
        transformed_dem = skimage.transform.warp(
            filled_dem, inds, order=resampling_order, mode="constant", cval=np.nan, preserve_range=True
        )
    
    
    
    
    "uint8"), inds, order=resampling_order, mode="constant", cval=1, preserve_range=True
    
    
    

    
    

    
    

    assert np.count_nonzero(~np.isnan(transformed_dem)) > 0, "Transformed DEM has all nans."

    return transformed_dem


class ZScaleCorr(Coreg):
    """
    Correct linear or nonlinear elevation scale errors.

    Often useful for nadir image DEM correction, where the focal length is slightly miscalculated.

    DISCLAIMER: This function may introduce error when correcting non-photogrammetric biases.
    See Gardelle et al. (2012) (Figure 2), http://dx.doi.org/10.3189/2012jog11j175, for curvature-related biases.
    """

    def __init__(self, degree: float = 1, bin_count: int = 100) -> None:
        """
        Instantiate a elevation scale correction object.

        :param degree: The polynomial degree to estimate.
        :param bin_count: The amount of bins to divide the elevation change in.
        """
        self.degree = degree
        self.bin_count = bin_count

        super().__init__()

    def _fit_func(
        self,
        ref_dem: NDArrayf,
        tba_dem: NDArrayf,
        transform: rio.transform.Affine | None,
        weights: NDArrayf | None,
        verbose: bool = False,
    ) -> None:
        """Estimate the scale difference between the two DEMs."""
        ddem = ref_dem - tba_dem

        medians = xdem.volume.hypsometric_binning(ddem=ddem, ref_dem=tba_dem, bins=self.bin_count, kind="count")[
            "value"
        ]

        coefficients = np.polyfit(medians.index.mid, medians.values, deg=self.degree)
        self._meta["coefficients"] = coefficients

    def _apply_func(self, dem: NDArrayf, transform: rio.transform.Affine, **kwargs: Any) -> NDArrayf:
        """Apply the scaling model to a DEM."""
        model = np.poly1d(self._meta["coefficients"])

        return dem + model(dem)

    def _apply_pts_func(self, coords: NDArrayf) -> NDArrayf:
        """Apply the scaling model to a set of points."""
        model = np.poly1d(self._meta["coefficients"])

        new_coords = coords.copy()
        new_coords[:, 2] += model(new_coords[:, 2])
        return new_coords

    def _to_matrix_func(self) -> NDArrayf:
        """Convert the transform to a matrix, if possible."""
        if self.degree == 0:  
            return self._meta["coefficients"][-1]
        elif self.degree < 2:
            raise NotImplementedError
        else:
            raise ValueError("A 2nd degree or higher ZScaleCorr cannot be described as a 4x4 matrix!")


class BlockwiseCoreg(Coreg):
    """
    Block-wise coreg class for nonlinear estimations.

    A coreg class of choice is run on an arbitrary subdivision of the raster. When later applying the coregistration,\
        the optimal warping is interpolated based on X/Y/Z shifts from the coreg algorithm at the grid points.

    E.g. a subdivision of 4 means to divide the DEM in four equally sized parts. These parts are then coregistered\
        separately, creating four Coreg.fit results. If the subdivision is not divisible by the raster shape,\
        subdivision is made as best as possible to have approximately equal pixel counts.
    """

    def __init__(
        self,
        coreg: Coreg | CoregPipeline,
        subdivision: int,
        success_threshold: float = 0.8,
        n_threads: int | None = None,
        warn_failures: bool = False,
    ) -> None:
        """
        Instantiate a blockwise coreg object.

        :param coreg: An instantiated coreg object to fit in the subdivided DEMs.
        :param subdivision: The number of chunks to divide the DEMs in. E.g. 4 means four different transforms.
        :param success_threshold: Raise an error if fewer chunks than the fraction failed for any reason.
        :param n_threads: The maximum amount of threads to use. Default=auto
        :param warn_failures: Trigger or ignore warnings for each exception/warning in each block.
        """
        if isinstance(coreg, type):
            raise ValueError(
                "The 'coreg' argument must be an instantiated Coreg subclass. " "Hint: write e.g. ICP() instead of ICP"
            )
        self.coreg = coreg
        self.subdivision = subdivision
        self.success_threshold = success_threshold
        self.n_threads = n_threads
        self.warn_failures = warn_failures

        super().__init__()

        self._meta: CoregDict = {"coreg_meta": []}

    def _fit_func(
        self,
        ref_dem: NDArrayf,
        tba_dem: NDArrayf,
        transform: rio.transform.Affine,
        weights: NDArrayf | None,
        verbose: bool = False,
    ) -> None:
        """Fit the coreg approach for each subdivision."""

        groups = self.subdivide_array(tba_dem.shape)

        indices = np.unique(groups)

        progress_bar = tqdm(total=indices.size, desc="Coregistering chunks", disable=(not verbose))

        def coregister(i: int) -> dict[str, Any] | BaseException | None:
            """
            Coregister a chunk in a thread-safe way.

            :returns:
                * If it succeeds: A dictionary of the fitting metadata.
                * If it fails: The associated exception.
                * If the block is empty: None
            """
            inlier_mask = groups == i

            
            rows, cols = np.where(inlier_mask)
            arrayslice = np.s_[rows.min() : rows.max() + 1, cols.min() : cols.max() + 1]

            
            ref_subset = ref_dem[arrayslice].copy()
            tba_subset = tba_dem[arrayslice].copy()

            if any(np.all(~np.isfinite(dem)) for dem in (ref_subset, tba_subset)):
                return None
            mask_subset = inlier_mask[arrayslice].copy()
            west, top = rio.transform.xy(transform, min(rows), min(cols), offset="ul")
            transform_subset = rio.transform.from_origin(west, top, transform.a, -transform.e)
            coreg = self.coreg.copy()

            
            try:
                coreg.fit(
                    reference_dem=ref_subset,
                    dem_to_be_aligned=tba_subset,
                    transform=transform_subset,
                    inlier_mask=mask_subset,
                )

                nmad, median = coreg.error(
                    reference_dem=ref_subset,
                    dem_to_be_aligned=tba_subset,
                    error_type=["nmad", "median"],
                    inlier_mask=mask_subset,
                    transform=transform_subset,
                )
            except Exception as exception:
                return exception

            meta: dict[str, Any] = {
                "i": i,
                "transform": transform_subset,
                "inlier_count": np.count_nonzero(mask_subset & np.isfinite(ref_subset) & np.isfinite(tba_subset)),
                "nmad": nmad,
                "median": median,
            }
            
            inlier_positions = np.argwhere(mask_subset)
            mid_row = np.mean(inlier_positions[:, 0]).astype(int)
            mid_col = np.mean(inlier_positions[:, 1]).astype(int)

            
            finites = np.argwhere(np.isfinite(tba_subset) & mask_subset)
            
            distances = np.linalg.norm(finites - np.array([mid_row, mid_col]), axis=1)
            
            closest = np.argwhere(distances == distances.min())

            
            representative_row, representative_col = finites[closest][0][0]
            meta["representative_x"], meta["representative_y"] = rio.transform.xy(
                transform_subset, representative_row, representative_col
            )
            meta["representative_val"] = ref_subset[representative_row, representative_col]

            
            if hasattr(coreg, "pipeline"):
                meta["pipeline"] = [step._meta.copy() for step in coreg.pipeline]

            "i", "min_row", etc, and the
            "coreg_meta" key)
            
            meta.update(
                {key: value for key, value in coreg._meta.items() if key not in ["coreg_meta"] + list(meta.keys())}
            )

            progress_bar.update()

            return meta.copy()

        
        exceptions: list[BaseException | warnings.WarningMessage] = []
        with warnings.catch_warnings(record=True) as caught_warnings:
            warnings.simplefilter("default")
            with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
                results = executor.map(coregister, indices)

            exceptions += list(caught_warnings)

        empty_blocks = 0
        for result in results:
            if isinstance(result, BaseException):
                exceptions.append(result)
            elif result is None:
                empty_blocks += 1
                continue
            else:
                self._meta["coreg_meta"].append(result)

        progress_bar.close()

        
        if ((len(self._meta["coreg_meta"]) + empty_blocks) / self.subdivision) <= self.success_threshold:
            raise ValueError(
                f"Fitting failed for {len(exceptions)} chunks:\n"
                + "\n".join(map(str, exceptions[:5]))
                + f"\n... and {len(exceptions) - 5} more"
                if len(exceptions) > 5
                else ""
            )

        if self.warn_failures:
            for exception in exceptions:
                warnings.warn(str(exception))

        
        self.coreg._fit_called = True
        if isinstance(self.coreg, CoregPipeline):
            for step in self.coreg.pipeline:
                step._fit_called = True

    def _restore_metadata(self, meta: CoregDict) -> None:
        """
        Given some metadata, set it in the right place.

        :param meta: A metadata file to update self._meta
        """
        self.coreg._meta.update(meta)

        if isinstance(self.coreg, CoregPipeline) and "pipeline" in meta:
            for i, step in enumerate(self.coreg.pipeline):
                step._meta.update(meta["pipeline"][i])

    def to_points(self) -> NDArrayf:
        """
        Convert the blockwise coregistration matrices to 3D (source -> destination) points.

        The returned shape is (N, 3, 2) where the dimensions represent:
            0. The point index where N is equal to the amount of subdivisions.
            1. The X/Y/Z coordinate of the point.
            2. The old/new position of the point.

        To acquire the first point's original position: points[0, :, 0]
        To acquire the first point's new position: points[0, :, 1]
        To acquire the first point's Z difference: points[0, 2, 1] - points[0, 2, 0]

        :returns: An array of 3D source -> destination points.
        """
        if len(self._meta["coreg_meta"]) == 0:
            raise AssertionError("No coreg results exist. Has '.fit()' been called?")
        points = np.empty(shape=(0, 3, 2))
        for meta in self._meta["coreg_meta"]:
            self._restore_metadata(meta)

            "transform"], meta["representative_row"],
            "representative_col"])
            x_coord, y_coord = meta["representative_x"], meta["representative_y"]

            old_position = np.reshape([x_coord, y_coord, meta["representative_val"]], (1, 3))
            new_position = self.coreg.apply_pts(old_position)

            points = np.append(points, np.dstack((old_position, new_position)), axis=0)

        return points

    def stats(self) -> pd.DataFrame:
        """
        Return statistics for each chunk in the blockwise coregistration.

            * center_{x,y,z}: The center coordinate of the chunk in georeferenced units.
            * {x,y,z}_off: The calculated offset in georeferenced units.
            * inlier_count: The number of pixels that were inliers in the chunk.
            * nmad: The NMAD after coregistration.
            * median: The bias after coregistration.

        :raises ValueError: If no coregistration results exist yet.

        :returns: A dataframe of statistics for each chunk.
        """
        points = self.to_points()

        chunk_meta = {meta["i"]: meta for meta in self._meta["coreg_meta"]}

        statistics: list[dict[str, Any]] = []
        for i in range(points.shape[0]):
            if i not in chunk_meta:
                continue
            statistics.append(
                {
                    "center_x": points[i, 0, 0],
                    "center_y": points[i, 1, 0],
                    "center_z": points[i, 2, 0],
                    "x_off": points[i, 0, 1] - points[i, 0, 0],
                    "y_off": points[i, 1, 1] - points[i, 1, 0],
                    "z_off": points[i, 2, 1] - points[i, 2, 0],
                    "inlier_count": chunk_meta[i]["inlier_count"],
                    "nmad": chunk_meta[i]["nmad"],
                    "median": chunk_meta[i]["median"],
                }
            )

        stats_df = pd.DataFrame(statistics)
        stats_df.index.name = "chunk"

        return stats_df

    def subdivide_array(self, shape: tuple[int, ...]) -> NDArrayf:
        """
        Return the grid subdivision for a given DEM shape.

        :param shape: The shape of the input DEM.

        :returns: An array of shape 'shape' with 'self.subdivision' unique indices.
        """
        if len(shape) == 3 and shape[0] == 1:  
            shape = (shape[1], shape[2])
        return spatial_tools.subdivide_array(shape, count=self.subdivision)

    def _apply_func(self, dem: NDArrayf, transform: rio.transform.Affine, **kwargs: Any) -> NDArrayf:

        points = self.to_points()

        bounds, resolution = _transform_to_bounds_and_res(dem.shape, transform)

        representative_height = np.nanmean(dem)
        edges_source = np.array(
            [
                [bounds.left + resolution / 2, bounds.top - resolution / 2, representative_height],
                [bounds.right - resolution / 2, bounds.top - resolution / 2, representative_height],
                [bounds.left + resolution / 2, bounds.bottom + resolution / 2, representative_height],
                [bounds.right - resolution / 2, bounds.bottom + resolution / 2, representative_height],
            ]
        )
        edges_dest = self.apply_pts(edges_source)
        edges = np.dstack((edges_source, edges_dest))

        all_points = np.append(points, edges, axis=0)

        warped_dem = warp_dem(
            dem=dem,
            transform=transform,
            source_coords=all_points[:, :, 0],
            destination_coords=all_points[:, :, 1],
            resampling="linear",
        )

        return warped_dem

    def _apply_pts_func(self, coords: NDArrayf) -> NDArrayf:
        """Apply the scaling model to a set of points."""
        points = self.to_points()

        new_coords = coords.copy()

        for dim in range(0, 3):
            with warnings.catch_warnings():
                
                warnings.filterwarnings("ignore", message="ZeroDivisionError")
                model = scipy.interpolate.Rbf(
                    points[:, 0, 0],
                    points[:, 1, 0],
                    points[:, dim, 1] - points[:, dim, 0],
                    function="linear",
                )

            new_coords[:, dim] += model(coords[:, 0], coords[:, 1])

        return new_coords


def warp_dem(
    dem: NDArrayf,
    transform: rio.transform.Affine,
    source_coords: NDArrayf,
    destination_coords: NDArrayf,
    resampling: str = "cubic",
    trim_border: bool = True,
    dilate_mask: bool = True,
) -> NDArrayf:
    """
    Warp a DEM using a set of source-destination 2D or 3D coordinates.

    :param dem: The DEM to warp. Allowed shapes are (1, row, col) or (row, col)
    :param transform: The Affine transform of the DEM.
    :param source_coords: The source 2D or 3D points. must be X/Y/(Z) coords of shape (N, 2) or (N, 3).
    :param destination_coords: The destination 2D or 3D points. Must have the exact same shape as 'source_coords'
    :param resampling: The resampling order to use. Choices: ['nearest', 'linear', 'cubic'].
    :param trim_border: Remove values outside of the interpolation regime (True) or leave them unmodified (False).
    :param dilate_mask: Dilate the nan mask to exclude edge pixels that could be wrong.

    :raises ValueError: If the inputs are poorly formatted.
    :raises AssertionError: For unexpected outputs.

    :returns: A warped DEM with the same shape as the input.
    """
    if source_coords.shape != destination_coords.shape:
        raise ValueError(
            f"Incompatible shapes: source_coords '({source_coords.shape})' and "
            f"destination_coords '({destination_coords.shape})' shapes must be the same"
        )
    if (len(source_coords.shape) > 2) or (source_coords.shape[1] < 2) or (source_coords.shape[1] > 3):
        raise ValueError(
            "Invalid coordinate shape. Expected 2D or 3D coordinates of shape (N, 2) or (N, 3). "
            f"Got '{source_coords.shape}'"
        )
    allowed_resampling_strs = ["nearest", "linear", "cubic"]
    if resampling not in allowed_resampling_strs:
        raise ValueError(f"Resampling type '{resampling}' not understood. Choices: {allowed_resampling_strs}")

    dem_arr, dem_mask = spatial_tools.get_array_and_mask(dem)

    bounds, resolution = _transform_to_bounds_and_res(dem_arr.shape, transform)

    no_horizontal = np.sum(np.linalg.norm(destination_coords[:, :2] - source_coords[:, :2], axis=1)) < 1e-6
    no_vertical = source_coords.shape[1] > 2 and np.sum(np.abs(destination_coords[:, 2] - source_coords[:, 2])) < 1e-6

    if no_horizontal and no_vertical:
        warnings.warn("No difference between source and destination coordinates. Returning self.")
        return dem

    source_coords_scaled = source_coords.copy()
    destination_coords_scaled = destination_coords.copy()
    
    for coords in (source_coords_scaled, destination_coords_scaled):
        coords[:, 0] = dem_arr.shape[1] * (coords[:, 0] - bounds.left) / (bounds.right - bounds.left)
        coords[:, 1] = dem_arr.shape[0] * (1 - (coords[:, 1] - bounds.bottom) / (bounds.top - bounds.bottom))

    
    grid_y, grid_x = np.mgrid[0 : dem_arr.shape[0], 0 : dem_arr.shape[1]]

    if no_horizontal:
        warped = dem_arr.copy()
    else:
        
        
        
        new_indices = scipy.interpolate.griddata(
            source_coords_scaled[:, [1, 0]],
            destination_coords_scaled[:, [1, 0]],  
            (grid_y, grid_x),
            method="linear",
        )

        
        if not trim_border:
            missing_ys = np.isnan(new_indices[:, :, 0])
            missing_xs = np.isnan(new_indices[:, :, 1])
            new_indices[:, :, 0][missing_ys] = grid_y[missing_ys]
            new_indices[:, :, 1][missing_xs] = grid_x[missing_xs]

        order = {"nearest": 0, "linear": 1, "cubic": 3}

        with warnings.catch_warnings():
            
            warnings.filterwarnings("ignore", message="Passing `np.nan` to mean no clipping in np.clip")
            warped = skimage.transform.warp(
                image=np.where(dem_mask, np.nan, dem_arr),
                inverse_map=np.moveaxis(new_indices, 2, 0),
                output_shape=dem_arr.shape,
                preserve_range=True,
                order=order[resampling],
                cval=np.nan,
            )
            new_mask = (
                skimage.transform.warp(
                    image=dem_mask, inverse_map=np.moveaxis(new_indices, 2, 0), output_shape=dem_arr.shape, cval=False
                )
                > 0
            )

        if dilate_mask:
            new_mask = scipy.ndimage.binary_dilation(new_mask, iterations=order[resampling]).astype(new_mask.dtype)

        warped[new_mask] = np.nan

    
    if not no_vertical:
        grid_offsets = scipy.interpolate.griddata(
            points=destination_coords_scaled[:, :2],
            values=destination_coords_scaled[:, 2] - source_coords_scaled[:, 2],
            xi=(grid_x, grid_y),
            method=resampling,
            fill_value=np.nan,
        )
        if not trim_border:
            grid_offsets[np.isnan(grid_offsets)] = np.nanmean(grid_offsets)

        warped += grid_offsets

    assert not np.all(np.isnan(warped)), "All-NaN output."

    return warped.reshape(dem.shape)


hmodes_dict = {
    "nuth_kaab": NuthKaab(),
    "nuth_kaab_block": BlockwiseCoreg(coreg=NuthKaab(), subdivision=16),
    "icp": ICP(),
}

vmodes_dict = {
    "median": BiasCorr(bias_func=np.median),
    "mean": BiasCorr(bias_func=np.mean),
    "deramp": Deramp(),
}


def dem_coregistration(
    src_dem_path: str,
    ref_dem_path: str,
    out_dem_path: str | None = None,
    shpfile: str | None = None,
    coreg_method: Coreg | None = None,
    hmode: str = "nuth_kaab",
    vmode: str = "median",
    deramp_degree: int = 1,
    grid: str = "ref",
    filtering: bool = True,
    slope_lim: list[AnyNumber] | tuple[AnyNumber, AnyNumber] = (0.1, 40),
    plot: bool = False,
    out_fig: str = None,
    verbose: bool = False,
) -> tuple[xdem.DEM, pd.DataFrame]:
    """
    A one-line function to coregister a selected DEM to a reference DEM.
    Reads both DEMs, reprojects them on the same grid, mask content of shpfile, filter steep slopes and outliers, \
run the coregistration, returns the coregistered DEM and some statistics.
    Optionally, save the coregistered DEM to file and make a figure.

    :param src_dem_path: path to the input DEM to be coregistered
    :param ref_dem: path to the reference DEM
    :param out_dem_path: Path where to save the coregistered DEM. If set to None (default), will not save to file.
    :param shpfile: path to a vector file containing areas to be masked for coregistration
    :param coreg_method: The xdem coregistration method, or pipeline. If set to None, DEMs will be resampled to \
ref grid and optionally filtered, but not coregistered. Will be used in priority over hmode and vmode.
    :param hmode: The method to be used for horizontally aligning the DEMs, e.g. Nuth & Kaab or ICP. Can be any \
of {list(vmodes_dict.keys())}.
    :param vmode: The method to be used for vertically aligning the DEMs, e.g. mean/median bias correction or \
deramping. Can be any of {list(hmodes_dict.keys())}.
    :param deramp_degree: The degree of the polynomial for deramping.
    :param grid: the grid to be used during coregistration, set either to "ref" or "src".
    :param filtering: if set to True, filtering will be applied prior to coregistration
    :param plot: Set to True to plot a figure of elevation diff before/after coregistration
    :param out_fig: Path to the output figure. If None will display to screen.
    :param verbose: set to True to print details on screen during coregistration.

    :returns: a tuple containing 1) coregistered DEM as an xdem.DEM instance and 2) DataFrame of coregistration \
statistics (count of obs, median and NMAD over stable terrain) before and after coreg.
    """
    
    if (coreg_method is not None) and ((hmode is not None) or (vmode is not None)):
        warnings.warn("Both `coreg_method` and `hmode/vmode` are set. Using coreg_method.")

    if hmode not in list(hmodes_dict.keys()):
        raise ValueError(f"vhmode must be in {list(hmodes_dict.keys())}")

    if vmode not in list(vmodes_dict.keys()):
        raise ValueError(f"vmode must be in {list(vmodes_dict.keys())}")

    
    if verbose:
        print("Loading and reprojecting input data")
    if grid == "ref":
        ref_dem, src_dem = gu.spatial_tools.load_multiple_rasters([ref_dem_path, src_dem_path], ref_grid=0)
    elif grid == "src":
        ref_dem, src_dem = gu.spatial_tools.load_multiple_rasters([ref_dem_path, src_dem_path], ref_grid=1)
    else:
        raise ValueError(f"`grid` must be either 'ref' or 'src' - currently set to {grid}")

    
    ref_dem = xdem.DEM(ref_dem.astype(np.float32))
    src_dem = xdem.DEM(src_dem.astype(np.float32))

    
    if shpfile is not None:
        outlines = gu.Vector(shpfile)
        stable_mask = ~outlines.create_mask(src_dem)
    else:
        stable_mask = np.ones(src_dem.data.shape, dtype="bool")

    
    ddem = src_dem - ref_dem

    
    if filtering:
        
        inlier_mask = stable_mask & (np.abs(ddem.data - np.median(ddem)) < 5 * xdem.spatialstats.nmad(ddem)).filled(
            False
        )

        
        slope = xdem.terrain.slope(ref_dem)
        inlier_mask[slope.data < slope_lim[0]] = False
        inlier_mask[slope.data > slope_lim[1]] = False

    else:
        inlier_mask = stable_mask

    
    inlier_data = ddem.data[inlier_mask].compressed()
    nstable_orig, mean_orig = len(inlier_data), np.mean(inlier_data)
    med_orig, nmad_orig = np.median(inlier_data), xdem.spatialstats.nmad(inlier_data)

    
    
    if isinstance(coreg_method, xdem.coreg.Coreg):
        coreg_method.fit(ref_dem, src_dem, inlier_mask, verbose=verbose)
        dem_coreg = coreg_method.apply(src_dem, dilate_mask=False)
    elif coreg_method is None:
        
        hcoreg_method = hmodes_dict[hmode]
        hcoreg_method.fit(ref_dem, src_dem, inlier_mask, verbose=verbose)
        dem_hcoreg = hcoreg_method.apply(src_dem, dilate_mask=False)

        
        vcoreg_method = vmodes_dict[vmode]
        if vmode == "deramp":
            vcoreg_method.degree = deramp_degree
        vcoreg_method.fit(ref_dem, dem_hcoreg, inlier_mask, verbose=verbose)
        dem_coreg = vcoreg_method.apply(dem_hcoreg, dilate_mask=False)

    ddem_coreg = dem_coreg - ref_dem

    
    inlier_data = ddem_coreg.data[inlier_mask].compressed()
    nstable_coreg, mean_coreg = len(inlier_data), np.mean(inlier_data)
    med_coreg, nmad_coreg = np.median(inlier_data), xdem.spatialstats.nmad(inlier_data)

    
    if plot:
        
        vmax = np.percentile(np.abs(ddem.data.compressed()), 98) // 5 * 5

        plt.figure(figsize=(11, 5))

        ax1 = plt.subplot(121)
        plt.imshow(ddem.data.squeeze(), cmap="coolwarm_r", vmin=-vmax, vmax=vmax)
        cb = plt.colorbar()
        cb.set_label("Elevation change (m)")
        ax1.set_title(f"Before coreg\n\nmean = {mean_orig:.1f} m - med = {med_orig:.1f} m - NMAD = {nmad_orig:.1f} m")

        ax2 = plt.subplot(122, sharex=ax1, sharey=ax1)
        plt.imshow(ddem_coreg.data.squeeze(), cmap="coolwarm_r", vmin=-vmax, vmax=vmax)
        cb = plt.colorbar()
        cb.set_label("Elevation change (m)")
        ax2.set_title(
            f"After coreg\n\n\nmean = {mean_coreg:.1f} m - med = {med_coreg:.1f} m - NMAD = {nmad_coreg:.1f} m"
        )

        plt.tight_layout()
        if out_fig is None:
            plt.show()
        else:
            plt.savefig(out_fig, dpi=200)
            plt.close()

    
    if out_dem_path is not None:
        dem_coreg.save(out_dem_path, tiled=True)

    
    out_stats = pd.DataFrame(
        ((nstable_orig, med_orig, nmad_orig, nstable_coreg, med_coreg, nmad_coreg),),
        columns=("nstable_orig", "med_orig", "nmad_orig", "nstable_coreg", "med_coreg", "nmad_coreg"),
    )

    return dem_coreg, out_stats
