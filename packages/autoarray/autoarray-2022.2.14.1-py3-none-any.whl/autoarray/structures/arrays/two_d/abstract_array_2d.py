import logging
import numpy as np
from typing import List, Tuple, Union

from autoarray.structures.abstract_structure import AbstractStructure2D

from autoarray.structures.arrays.one_d.array_1d import Array1D
from autoarray.mask.mask_2d import Mask2D

from autoarray import exc
from autoarray.structures.arrays import abstract_array
from autoarray.structures.arrays.two_d import array_2d_util
from autoarray.layout import layout_util


logging.basicConfig()
logger = logging.getLogger(__name__)


def check_array_2d(array_2d: np.ndarray):
    if len(array_2d.shape) != 1:
        raise exc.ArrayException(
            "An array input into the Array2D.__new__ method is not of shape 1."
        )


def convert_array_2d(array_2d: Union[np.ndarray, List], mask_2d: Mask2D) -> np.ndarray:
    """
    The `manual` classmethods in the `Array2D` object take as input a list or ndarray which is returned as an
    Array2D.

    This function performs the following and checks and conversions on the input:

    1) If the input is a list, convert it to an ndarray.
    2) Check that the number of sub-pixels in the array is identical to that of the mask.
    3) Map the input ndarray to its `slim` representation.

    For an Array2D, `slim` refers to a 1D NumPy array of shape [total_values] and `native` a 2D NumPy array of shape
    [total_y_values, total_values].

    Parameters
    ----------
    array_2d
        The input structure which is converted to an ndarray if it is a list.
    mask_2d
        The mask of the output Array2D.
    """

    array_2d = abstract_array.convert_array(array=array_2d)

    return convert_array_2d_to_slim(array_2d=array_2d, mask_2d=mask_2d)


def convert_array_2d_to_slim(array_2d: np.ndarray, mask_2d: Mask2D) -> np.ndarray:
    """
    The `manual` classmethods in the `Array2D` object take as input a list or ndarray which is returned as an
    Array2D.

    This function checks the dimensions of the input `array_2d` and maps it to its `slim` representation.

    For an Array2D, `slim` refers to a 1D NumPy array of shape [total_values].

    Parameters
    ----------
    array_2d
        The input structure which is converted to its slim representation.
    mask_2d
        The mask of the output Array2D.
    """

    if len(array_2d.shape) == 1:

        array_2d_slim = array_2d

        if array_2d_slim.shape[0] != mask_2d.sub_pixels_in_mask:
            raise exc.ArrayException(
                "The input 1D array does not have the same number of entries as sub-pixels in"
                "the mask."
            )

        return array_2d_slim

    if array_2d.shape != mask_2d.sub_shape_native:
        raise exc.ArrayException(
            "The input array is 2D but not the same dimensions as the sub-mask "
            "(e.g. the mask 2D shape multipled by its sub size.)"
        )

    return array_2d_util.array_2d_slim_from(
        array_2d_native=array_2d, mask_2d=mask_2d, sub_size=mask_2d.sub_size
    )


def convert_array_2d_to_native(array_2d: np.ndarray, mask_2d: Mask2D) -> np.ndarray:
    """
    The `manual` classmethods in the `Array2D` object take as input a list or ndarray which is returned as an
    Array2D.

    This function checks the dimensions of the input `array_2d` and maps it to its `native` representation.

    For an Array2D, `native` a 2D NumPy array of shape [total_y_values, total_values].

    Parameters
    ----------
    array_2d
        The input structure which is converted to an ndarray if it is a list.
    mask_2d : Mask2D
        The mask of the output Array2D.
    """

    if len(array_2d.shape) == 2:

        array_2d_native = array_2d * np.invert(mask_2d)

        if array_2d.shape != mask_2d.sub_shape_native:
            raise exc.ArrayException(
                "The input array is 2D but not the same dimensions as the sub-mask "
                "(e.g. the mask 2D shape multipled by its sub size.)"
            )

        return array_2d_native

    if array_2d.shape[0] != mask_2d.sub_pixels_in_mask:
        raise exc.ArrayException(
            "The input 1D array does not have the same number of entries as sub-pixels in"
            "the mask."
        )

    return array_2d_util.array_2d_native_from(
        array_2d_slim=array_2d, mask_2d=mask_2d, sub_size=mask_2d.sub_size
    )


class AbstractArray2D(AbstractStructure2D):

    header = None

    def _new_structure(
        self, array: "AbstractArray2D", mask: Mask2D
    ) -> "AbstractArray2D":
        return self.__class__(array=array, mask=mask, header=self.header)

    @property
    def slim(self) -> Union["AbstractArray2D", "Array2D"]:
        """
        Return an `Array2D` where the data is stored its `slim` representation, which is an ndarray of shape
        [total_unmasked_pixels * sub_size**2].

        If it is already stored in its `slim` representation it is returned as it is. If not, it is  mapped from
        `native` to `slim` and returned as a new `Array2D`.
        """

        if len(self.shape) == 1:
            return self

        sub_array_1d = array_2d_util.array_2d_slim_from(
            array_2d_native=self, mask_2d=self.mask, sub_size=self.mask.sub_size
        )

        return self._new_structure(array=sub_array_1d, mask=self.mask)

    @property
    def native(self) -> Union["AbstractArray2D", "Array2D"]:
        """
        Return a `Array2D` where the data is stored in its `native` representation, which is an ndarray of shape
        [sub_size*total_y_pixels, sub_size*total_x_pixels].

        If it is already stored in its `native` representation it is return as it is. If not, it is mapped from
        `slim` to `native` and returned as a new `Array2D`.
        """

        if len(self.shape) != 1:
            return self

        sub_array_2d = array_2d_util.array_2d_native_from(
            array_2d_slim=self, mask_2d=self.mask, sub_size=self.mask.sub_size
        )
        return self._new_structure(array=sub_array_2d, mask=self.mask)

    @property
    def binned(self) -> Union["AbstractArray2D", "Array2D"]:
        """
        Convenience method to access the binned-up array in its 1D representation, which is a Grid2D stored as an
        ndarray of shape [total_unmasked_pixels, 2].

        The binning up process converts a array from (y,x) values where each value is a coordinate on the sub-array to
        (y,x) values where each coordinate is at the centre of its mask (e.g. a array with a sub_size of 1). This is
        performed by taking the mean of all (y,x) values in each sub pixel.

        If the array is stored in 1D it is return as is. If it is stored in 2D, it must first be mapped from 2D to 1D.
        """

        array_2d_slim = self.slim

        binned_array_1d = np.multiply(
            self.mask.sub_fraction,
            array_2d_slim.reshape(-1, self.mask.sub_length).sum(axis=1),
        )

        return self._new_structure(array=binned_array_1d, mask=self.mask.mask_sub_1)

    @property
    def extent(self) -> np.ndarray:
        return self.mask.extent

    @property
    def in_counts(self) -> "AbstractArray2D":
        return self.header.array_eps_to_counts(array_eps=self)

    @property
    def in_counts_per_second(self) -> "AbstractArray2D":
        return self.header.array_counts_to_counts_per_second(
            array_counts=self.in_counts
        )

    @property
    def original_orientation(self) -> Union[np.ndarray, "AbstractArray2D"]:
        return layout_util.rotate_array_via_roe_corner_from(
            array=self, roe_corner=self.header.original_roe_corner
        )

    @property
    def readout_offsets(self) -> Tuple[int, int]:
        if self.header is not None:
            if self.header.readout_offsets is not None:
                return self.header.readout_offsets
        return (0, 0)

    @property
    def binned_across_rows(self) -> Array1D:
        binned_array = np.mean(np.ma.masked_array(self.native, self.mask), axis=0)
        return Array1D.manual_native(array=binned_array, pixel_scales=self.pixel_scale)

    @property
    def binned_across_columns(self) -> Array1D:
        binned_array = np.mean(np.ma.masked_array(self.native, self.mask), axis=1)
        return Array1D.manual_native(array=binned_array, pixel_scales=self.pixel_scale)

    def zoomed_around_mask(self, buffer: int = 1) -> "AbstractArray2D":
        """
        Extract the 2D region of an array corresponding to the rectangle encompassing all unmasked values.

        This is used to extract and visualize only the region of an image that is used in an analysis.

        Parameters
        ----------
        buffer
            The number pixels around the extracted array used as a buffer.
        """

        extracted_array_2d = array_2d_util.extracted_array_2d_from(
            array_2d=self.native,
            y0=self.mask.zoom_region[0] - buffer,
            y1=self.mask.zoom_region[1] + buffer,
            x0=self.mask.zoom_region[2] - buffer,
            x1=self.mask.zoom_region[3] + buffer,
        )

        mask = Mask2D.unmasked(
            shape_native=extracted_array_2d.shape,
            pixel_scales=self.pixel_scales,
            sub_size=self.sub_size,
            origin=self.mask.mask_centre,
        )

        array = convert_array_2d(array_2d=extracted_array_2d, mask_2d=mask)

        return self._new_structure(array=array, mask=mask)

    def extent_of_zoomed_array(self, buffer: int = 1) -> np.ndarray:
        """
        For an extracted zoomed array computed from the method *zoomed_around_mask* compute its extent in scaled
        coordinates.

        The extent of the grid in scaled units returned as an ndarray of the form [x_min, x_max, y_min, y_max].

        This is used visualize zoomed and extracted arrays via the imshow() method.

        Parameters
        ----------
        buffer
            The number pixels around the extracted array used as a buffer.
        """
        extracted_array_2d = array_2d_util.extracted_array_2d_from(
            array_2d=self.native,
            y0=self.mask.zoom_region[0] - buffer,
            y1=self.mask.zoom_region[1] + buffer,
            x0=self.mask.zoom_region[2] - buffer,
            x1=self.mask.zoom_region[3] + buffer,
        )

        mask = Mask2D.unmasked(
            shape_native=extracted_array_2d.shape,
            pixel_scales=self.pixel_scales,
            sub_size=self.sub_size,
            origin=self.mask.mask_centre,
        )

        return mask.extent

    def resized_from(
        self, new_shape: Tuple[int, int], mask_pad_value: int = 0.0
    ) -> "AbstractArray2D":
        """
        Resize the array around its centre to a new input shape.

        If a new_shape dimension is smaller than the current dimension, the data at the edges is trimmed and removed.
        If it is larger, the data is padded with zeros.

        If the array has even sized dimensions, the central pixel around which data is trimmed / padded is chosen as
        the top-left pixel of the central quadrant of pixels.

        Parameters
        -----------
        new_shape
            The new 2D shape of the array.
        """

        resized_array_2d = array_2d_util.resized_array_2d_from(
            array_2d=self.native, resized_shape=new_shape
        )

        resized_mask = self.mask.resized_mask_from(
            new_shape=new_shape, pad_value=mask_pad_value
        )

        array = convert_array_2d(array_2d=resized_array_2d, mask_2d=resized_mask)

        return self._new_structure(array=array, mask=resized_mask)

    def padded_before_convolution_from(
        self, kernel_shape: Tuple[int, int], mask_pad_value: int = 0.0
    ) -> "AbstractArray2D":
        """
        When the edge pixels of a mask are unmasked and a convolution is to occur, the signal of edge pixels will be
        'missing' if the grid is used to evaluate the signal via an analytic function.

        To ensure this signal is included the array can be padded, where it is 'buffed' such that it includes all
        pixels whose signal will be convolved into the unmasked pixels given the 2D kernel shape. The values of
        these pixels are zeros.

        Parameters
        ----------
        kernel_shape
            The 2D shape of the kernel which convolves signal from masked pixels to unmasked pixels.
        """
        new_shape = (
            self.shape_native[0] + (kernel_shape[0] - 1),
            self.shape_native[1] + (kernel_shape[1] - 1),
        )
        return self.resized_from(new_shape=new_shape, mask_pad_value=mask_pad_value)

    def trimmed_after_convolution_from(
        self, kernel_shape: Tuple[int, int]
    ) -> "AbstractArray2D":
        """
        When the edge pixels of a mask are unmasked and a convolution is to occur, the signal of edge pixels will be
        'missing' if the grid is used to evaluate the signal via an analytic function.

        To ensure this signal is included the array can be padded, a padded array can be computed via the method
        *padded_before_convolution_from*. This function trims the array back to its original shape, after the padded array
        has been used for computational.

        Parameters
        ----------
        kernel_shape
            The 2D shape of the kernel which convolves signal from masked pixels to unmasked pixels.
        """
        psf_cut_y = int(np.ceil(kernel_shape[0] / 2)) - 1
        psf_cut_x = int(np.ceil(kernel_shape[1] / 2)) - 1
        array_y = int(self.mask.shape[0])
        array_x = int(self.mask.shape[1])
        trimmed_array_2d = self.native[
            psf_cut_y : array_y - psf_cut_y, psf_cut_x : array_x - psf_cut_x
        ]

        resized_mask = self.mask.resized_mask_from(new_shape=trimmed_array_2d.shape)

        array = convert_array_2d(array_2d=trimmed_array_2d, mask_2d=resized_mask)

        return self.__class__(array=array, mask=resized_mask)

    def output_to_fits(self, file_path: str, overwrite: bool = False):
        """
        Output the array to a .fits file.

        Parameters
        ----------
        file_path
            The output path of the file, including the filename and the `.fits` extension e.g. '/path/to/filename.fits'
        overwrite
            If a file already exists at the path, if overwrite=True it is overwritten else an error is raised.
        """
        array_2d_util.numpy_array_2d_to_fits(
            array_2d=self.native, file_path=file_path, overwrite=overwrite
        )
