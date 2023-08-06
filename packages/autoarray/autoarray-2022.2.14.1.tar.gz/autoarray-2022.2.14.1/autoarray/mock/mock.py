import numpy as np
from typing import List, Tuple, Union

from autoarray.preloads import Preloads
from autoarray.inversion.linear_obj import LinearObjFunc
from autoarray.inversion.pixelizations.abstract import AbstractPixelization
from autoarray.inversion.regularization.abstract import AbstractRegularization
from autoarray.inversion.mappers.abstract import AbstractMapper
from autoarray.inversion.linear_eqn.imaging import AbstractLEqImaging
from autoarray.inversion.linear_eqn.abstract import AbstractLEq
from autoarray.inversion.inversion.matrices import InversionMatrices
from autoarray.inversion.inversion.settings import SettingsInversion
from autoarray.structures.grids.two_d.grid_2d_pixelization import PixelNeighbors


class MockMask:
    def __init__(self, native_index_for_slim_index=None):

        self.native_index_for_slim_index = native_index_for_slim_index


class MockDataset:
    def __init__(self, grid_inversion=None, psf=None, mask=None):

        self.grid_inversion = grid_inversion
        self.psf = psf
        self.mask = mask


class MockFit:
    def __init__(
        self,
        dataset=MockDataset(),
        inversion=None,
        noise_map=None,
        regularization_term=None,
        log_det_curvature_reg_matrix_term=None,
        log_det_regularization_matrix_term=None,
    ):

        self.dataset = dataset
        self.inversion = inversion
        self.noise_map = noise_map
        self.signal_to_noise_map = noise_map

        self.regularization_term = regularization_term
        self.log_det_curvature_reg_matrix_term = log_det_curvature_reg_matrix_term
        self.log_det_regularization_matrix_term = log_det_regularization_matrix_term


### LEq ###


class MockConvolver:
    def __init__(self, blurred_mapping_matrix=None):
        self.blurred_mapping_matrix = blurred_mapping_matrix

    def convolve_mapping_matrix(self, mapping_matrix):
        return self.blurred_mapping_matrix


class MockLinearObjFunc(LinearObjFunc):
    def __init__(
        self, grid=None, mapping_matrix=None, blurred_mapping_matrix_override=None
    ):

        super().__init__(grid=grid)

        self._mapping_matrix = mapping_matrix
        self._blurred_mapping_matrix_override = blurred_mapping_matrix_override

    @property
    def mapping_matrix(self) -> np.ndarray:
        return self._mapping_matrix

    @property
    def blurred_mapping_matrix_override(self) -> np.ndarray:
        return self._blurred_mapping_matrix_override


class MockPixelizationGrid:
    def __init__(self, pixel_neighbors=None, pixel_neighbors_sizes=None):

        self.pixel_neighbors = PixelNeighbors(
            arr=pixel_neighbors, sizes=pixel_neighbors_sizes
        )
        self.shape = (len(self.pixel_neighbors.sizes),)


class MockPixelization(AbstractPixelization):
    def __init__(self, mapper=None, data_pixelization_grid=None):

        super().__init__()

        self.mapper = mapper
        self.data_pixelization_grid = data_pixelization_grid

    # noinspection PyUnusedLocal,PyShadowingNames
    def mapper_from(
        self,
        source_grid_slim,
        source_pixelization_grid,
        data_pixelization_grid=None,
        hyper_image=None,
        settings=None,
        preloads=None,
        profiling_dict=None,
    ):
        return self.mapper

    def data_pixelization_grid_from(self, data_grid_slim, hyper_image, settings=None):

        if hyper_image is not None and self.data_pixelization_grid is not None:
            return hyper_image * self.data_pixelization_grid

        return self.data_pixelization_grid


class MockRegularization(AbstractRegularization):
    def __init__(self, regularization_matrix=None):

        super().__init__()

        self.regularization_matrix = regularization_matrix

    def regularization_matrix_via_pixel_neighbors_from(
        self, pixel_neighbors, pixel_neighbors_sizes
    ):
        return self.regularization_matrix

    def regularization_matrix_from(self, mapper):

        return self.regularization_matrix


class MockMapper(AbstractMapper):
    def __init__(
        self,
        source_grid_slim=None,
        source_pixelization_grid=None,
        hyper_image=None,
        pix_sub_weights=None,
        mapping_matrix=None,
        pixel_signals=None,
        pixels=None,
    ):

        super().__init__(
            source_grid_slim=source_grid_slim,
            source_pixelization_grid=source_pixelization_grid,
            hyper_image=hyper_image,
        )

        self._pix_sub_weights = pix_sub_weights

        self._mapping_matrix = mapping_matrix

        self._pixels = pixels

        self._pixel_signals = pixel_signals

    def pixel_signals_from(self, signal_scale):
        if self._pixel_signals is None:
            return super().pixel_signals_from(signal_scale=signal_scale)
        return self._pixel_signals

    @property
    def pixels(self):
        if self._pixels is None:
            return super().pixels
        return self._pixels

    @property
    def pix_sub_weights(self):
        return self._pix_sub_weights

    @property
    def mapping_matrix(self):
        return self._mapping_matrix


class MockLEq(AbstractLEq):
    def __init__(
        self,
        noise_map=None,
        linear_obj_list: List[Union[MockMapper]] = None,
        operated_mapping_matrix=None,
        data_vector=None,
        curvature_matrix=None,
        mapped_reconstructed_data_dict=None,
        mapped_reconstructed_image_dict=None,
    ):

        super().__init__(noise_map=noise_map, linear_obj_list=linear_obj_list)

        self._operated_mapping_matrix = operated_mapping_matrix
        self._data_vector = data_vector
        self._curvature_matrix = curvature_matrix
        self._mapped_reconstructed_data_dict = mapped_reconstructed_data_dict
        self._mapped_reconstructed_image_dict = mapped_reconstructed_image_dict

    @property
    def operated_mapping_matrix(self) -> np.ndarray:
        if self._operated_mapping_matrix is None:
            return super().operated_mapping_matrix

        return self._operated_mapping_matrix

    def data_vector_from(self, data) -> np.ndarray:
        if self._data_vector is None:
            return super().data_vector_from(data=data)

        return self._data_vector

    @property
    def curvature_matrix_diag(self):
        return self._curvature_matrix

    def mapped_reconstructed_data_dict_from(self, reconstruction: np.ndarray):
        """
        Using the reconstructed source pixel fluxes we map each source pixel flux back to the image plane and
        reconstruct the image data.

        This uses the unique mappings of every source pixel to image pixels, which is a quantity that is already
        computed when using the w-tilde formalism.

        Returns
        -------
        Array2D
            The reconstructed image data which the inversion fits.
        """

        if self._mapped_reconstructed_data_dict is None:
            return super().mapped_reconstructed_data_dict_from(
                reconstruction=reconstruction
            )

        return self._mapped_reconstructed_data_dict

    def mapped_reconstructed_image_dict_from(self, reconstruction: np.ndarray):
        """
        Using the reconstructed source pixel fluxes we map each source pixel flux back to the image plane and
        reconstruct the image image.

        This uses the unique mappings of every source pixel to image pixels, which is a quantity that is already
        computed when using the w-tilde formalism.

        Returns
        -------
        Array2D
            The reconstructed image image which the inversion fits.
        """

        if self._mapped_reconstructed_image_dict is None:
            return super().mapped_reconstructed_image_dict_from(
                reconstruction=reconstruction
            )

        return self._mapped_reconstructed_image_dict


class MockLEqImaging(AbstractLEqImaging):
    def __init__(
        self,
        noise_map=None,
        convolver=None,
        linear_obj_list=None,
        blurred_mapping_matrix=None,
    ):

        super().__init__(
            noise_map=noise_map, convolver=convolver, linear_obj_list=linear_obj_list
        )

        self._blurred_mapping_matrix = blurred_mapping_matrix

    @property
    def blurred_mapping_matrix(self):
        if self._blurred_mapping_matrix is None:
            return super().blurred_mapping_matrix

        return self._blurred_mapping_matrix


class MockInversion(InversionMatrices):
    def __init__(
        self,
        data=None,
        leq: MockLEq = None,
        regularization_list: List[MockRegularization] = None,
        data_vector=None,
        regularization_matrix=None,
        curvature_reg_matrix=None,
        reconstruction: np.ndarray = None,
        reconstruction_dict: List[np.ndarray] = None,
        log_det_regularization_matrix_term=None,
        curvature_matrix_preload=None,
        curvature_matrix_counts=None,
        settings: SettingsInversion = SettingsInversion(),
        preloads: Preloads = Preloads(),
    ):

        # self.__dict__["curvature_matrix"] = curvature_matrix
        # self.__dict__["curvature_reg_matrix_cholesky"] = curvature_reg_matrix_cholesky
        # self.__dict__["regularization_matrix"] = regularization_matrix
        # self.__dict__["curvature_reg_matrix"] = curvature_reg_matrix
        # self.__dict__["reconstruction"] = reconstruction
        # self.__dict__["mapped_reconstructed_image"] = mapped_reconstructed_image

        super().__init__(
            data=data,
            leq=leq,
            regularization_list=regularization_list,
            settings=settings,
            preloads=preloads,
        )

        self._data_vector = data_vector
        self._regularization_matrix = regularization_matrix
        self._curvature_reg_matrix = curvature_reg_matrix
        self._reconstruction = reconstruction
        self._reconstruction_dict = reconstruction_dict

        self._log_det_regularization_matrix_term = log_det_regularization_matrix_term

        self._curvature_matrix_preload = curvature_matrix_preload
        self._curvature_matrix_counts = curvature_matrix_counts

    @property
    def data_vector(self) -> np.ndarray:
        if self._data_vector is None:
            return super().data_vector
        return self._data_vector

    @property
    def regularization_matrix(self):

        if self._regularization_matrix is None:
            return super().regularization_matrix

        return self._regularization_matrix

    @property
    def curvature_reg_matrix(self):
        return self._curvature_reg_matrix

    @property
    def reconstruction(self):
        """
        Solve the linear system [F + reg_coeff*H] S = D -> S = [F + reg_coeff*H]^-1 D given by equation (12)
        of https://arxiv.org/pdf/astro-ph/0302587.pdf

        S is the vector of reconstructed inversion values.
        """

        if self._reconstruction is None:
            return super().reconstruction

        return self._reconstruction

    @property
    def reconstruction_dict(self):
        """
        Solve the linear system [F + reg_coeff*H] S = D -> S = [F + reg_coeff*H]^-1 D given by equation (12)
        of https://arxiv.org/pdf/astro-ph/0302587.pdf

        S is the vector of reconstructed inversion values.
        """

        if self._reconstruction_dict is None:
            return super().reconstruction_dict

        return self._reconstruction_dict

    @property
    def log_det_regularization_matrix_term(self):

        if self._log_det_regularization_matrix_term is None:
            return super().log_det_regularization_matrix_term

        return self._log_det_regularization_matrix_term

    @property
    def curvature_matrix_preload(self):
        if self._curvature_matrix_preload is None:
            return super().curvature_matrix_preload

        return self._curvature_matrix_preload

    @property
    def curvature_matrix_counts(self):
        if self._curvature_matrix_counts is None:
            return super().curvature_matrix_counts

        return self._curvature_matrix_counts
