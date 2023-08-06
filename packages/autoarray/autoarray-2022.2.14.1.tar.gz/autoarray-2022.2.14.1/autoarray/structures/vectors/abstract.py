import logging
import numpy as np

from autoarray.structures.abstract_structure import AbstractStructure2D

from autoarray.structures.grids.two_d.grid_2d import Grid2D
from autoarray.structures.grids.two_d import grid_2d_util

logging.basicConfig()
logger = logging.getLogger(__name__)


class AbstractVectorYX2D(AbstractStructure2D):
    def __array_finalize__(self, obj):

        if hasattr(obj, "mask"):
            self.mask = obj.mask

        if hasattr(obj, "grid"):
            self.grid = obj.grid

    @property
    def slim(self) -> "VectorYX2D":
        """
        Return a `VectorYX2D` where the data is stored its `slim` representation, which is an ndarray of shape
        [total_unmasked_pixels * sub_size**2, 2].

        If it is already stored in its `slim` representation it is returned as it is. If not, it is  mapped from
        `native` to `slim` and returned as a new `Array2D`.
        """
        if len(self.shape) == 2:
            return self

        vectors_2d_slim = grid_2d_util.grid_2d_slim_from(
            grid_2d_native=self, mask=self.mask, sub_size=self.mask.sub_size
        )

        return self.__class__(
            vectors=vectors_2d_slim, grid=self.grid.slim, mask=self.mask
        )

    @property
    def native(self) -> "VectorYX2D":
        """
        Return a `VectorYX2D` where the data is stored in its `native` representation, which is an ndarray of shape
        [sub_size*total_y_pixels, sub_size*total_x_pixels, 2].

        If it is already stored in its `native` representation it is return as it is. If not, it is mapped from
        `slim` to `native` and returned as a new `Grid2D`.
        """

        if len(self.shape) != 2:
            return self

        vectors_2d_native = grid_2d_util.grid_2d_native_from(
            grid_2d_slim=self, mask_2d=self.mask, sub_size=self.mask.sub_size
        )

        return self.__class__(
            vectors=vectors_2d_native, grid=self.grid.native, mask=self.mask
        )

    @property
    def binned(self) -> "VectorYX2D":
        """
        Convenience method to access the binned-up vectors as a Vector2D stored in its `slim` or `native` format.

        The binning up process converts a grid from (y,x) values where each value is a coordinate on the sub-grid to
        (y,x) values where each coordinate is at the centre of its mask (e.g. a grid with a sub_size of 1). This is
        performed by taking the mean of all (y,x) values in each sub pixel.

        If the grid is stored in 1D it is return as is. If it is stored in 2D, it must first be mapped from 2D to 1D.
        """

        vector_2d_slim_binned_y = np.multiply(
            self.mask.sub_fraction,
            self.slim[:, 0].reshape(-1, self.mask.sub_length).sum(axis=1),
        )

        vector_2d_slim_binned_x = np.multiply(
            self.mask.sub_fraction,
            self.slim[:, 1].reshape(-1, self.mask.sub_length).sum(axis=1),
        )

        return self.__class__(
            vectors=np.stack(
                (vector_2d_slim_binned_y, vector_2d_slim_binned_x), axis=-1
            ),
            grid=self.grid.binned,
            mask=self.mask.mask_sub_1,
        )

    @property
    def average_magnitude(self) -> float:
        """
        The average magnitude of the vector field, where averaging is performed on the (vector_y, vector_x) components.
        """
        return np.sqrt(np.mean(self.slim[:, 0]) ** 2 + np.mean(self.slim[:, 1]) ** 2)

    @property
    def average_phi(self) -> float:
        """
        The average angle of the vector field, where averaging is performed on the (vector_y, vector_x) components.
        """
        return (
            0.5
            * np.arctan2(np.mean(self.slim[:, 0]), np.mean(self.slim[:, 1]))
            * (180 / np.pi)
        )
