"""Joint-density of states calculation."""
# Copyright (C) 2020 Atsushi Togo
# All rights reserved.
#
# This file is part of phono3py.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in
#   the documentation and/or other materials provided with the
#   distribution.
#
# * Neither the name of the phonopy project nor the names of its
#   contributors may be used to endorse or promote products derived
#   from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import sys
import warnings

import numpy as np
from phonopy.harmonic.dynamical_matrix import DynamicalMatrix, get_dynamical_matrix
from phonopy.structure.cells import Primitive
from phonopy.structure.tetrahedron_method import TetrahedronMethod
from phonopy.units import VaspToTHz

from phono3py.phonon3.imag_self_energy import get_frequency_points
from phono3py.phonon3.triplets import (
    get_nosym_triplets_at_q,
    get_tetrahedra_vertices,
    get_triplets_at_q,
    get_triplets_integration_weights,
)
from phono3py.phonon.func import bose_einstein
from phono3py.phonon.grid import BZGrid
from phono3py.phonon.solver import run_phonon_solver_c


class JointDos:
    """Calculate joint-density-of-states."""

    def __init__(
        self,
        primitive,
        supercell,
        bz_grid,
        fc2,
        nac_params=None,
        nac_q_direction=None,
        sigma=None,
        cutoff_frequency=None,
        frequency_step=None,
        num_frequency_points=None,
        temperatures=None,
        frequency_factor_to_THz=VaspToTHz,
        frequency_scale_factor=1.0,
        is_mesh_symmetry=True,
        store_dense_gp_map=False,
        symprec=1e-5,
        filename=None,
        log_level=False,
        lapack_zheev_uplo="L",
    ):
        """Init method."""
        self._grid_point = None
        self._primitive = primitive
        self._supercell = supercell
        self._bz_grid = bz_grid
        self._fc2 = fc2
        self._nac_params = nac_params
        self.nac_q_direction = nac_q_direction
        self._sigma = None
        self.set_sigma(sigma)

        if cutoff_frequency is None:
            self._cutoff_frequency = 0
        else:
            self._cutoff_frequency = cutoff_frequency
        self._frequency_step = frequency_step
        self._num_frequency_points = num_frequency_points
        self._temperatures = temperatures
        self._frequency_factor_to_THz = frequency_factor_to_THz
        self._frequency_scale_factor = frequency_scale_factor
        self._is_mesh_symmetry = is_mesh_symmetry
        self._store_dense_gp_map = store_dense_gp_map
        self._symprec = symprec
        self._filename = filename
        self._log_level = log_level
        self._lapack_zheev_uplo = lapack_zheev_uplo

        self._num_band = len(self._primitive) * 3
        self._reciprocal_lattice = np.linalg.inv(self._primitive.cell)
        self._init_dynamical_matrix()

        self._tetrahedron_method = None
        self._phonon_done = None
        self._frequencies = None
        self._eigenvectors = None

        self._joint_dos = None
        self._frequency_points = None

    def run(self):
        """Calculate joint-density-of-states."""
        self.run_phonon_solver(np.arange(len(self._bz_grid.addresses), dtype="int_"))
        try:
            import phono3py._phono3py as phono3c  # noqa F401

            self._run_c()
        except ImportError:
            print("Joint density of states in python is not implemented.")
            return None, None

    @property
    def dynamical_matrix(self) -> DynamicalMatrix:
        """Return dynamical matrix class instance."""
        return self._dm

    @property
    def joint_dos(self):
        """Return joint-density-of-states."""
        return self._joint_dos

    def get_joint_dos(self):
        """Return joint-density-of-states."""
        warnings.warn("Use attribute, joint_dos", DeprecationWarning)
        return self.joint_dos

    @property
    def frequency_points(self):
        """Getter and setter of frequency points."""
        return self._frequency_points

    @frequency_points.setter
    def frequency_points(self, frequency_points):
        self._frequency_points = np.array(frequency_points, dtype="double")

    def get_frequency_points(self):
        """Return frequency points."""
        warnings.warn("Use attribute, frequency_points", DeprecationWarning)
        return self.frequency_points

    def get_phonons(self):
        """Return phonon calculation results."""
        return self._frequencies, self._eigenvectors, self._phonon_done

    @property
    def primitive(self) -> Primitive:
        """Return primitive cell."""
        return self._primitive

    def get_primitive(self):
        """Return primitive cell."""
        warnings.warn("Use attribute, primitive", DeprecationWarning)
        return self.primitive

    @property
    def mesh_numbers(self):
        """Return mesh numbers by three integer values."""
        return self._bz_grid.D_diag

    def get_mesh_numbers(self):
        """Return mesh numbers by three integer values."""
        warnings.warn("Use attribute, mesh_numbers", DeprecationWarning)
        return self.mesh

    @property
    def nac_q_direction(self):
        """Getter and setter of q-direction for NAC."""
        return self._nac_q_direction

    @nac_q_direction.setter
    def nac_q_direction(self, nac_q_direction=None):
        if nac_q_direction is None:
            self._nac_q_direction = None
        else:
            self._nac_q_direction = np.array(nac_q_direction, dtype="double")

    def set_nac_q_direction(self, nac_q_direction=None):
        """Set q-direction for NAC."""
        warnings.warn("Use attribute, nac_q_direction", DeprecationWarning)
        self.nac_q_direction = nac_q_direction

    def set_sigma(self, sigma):
        """Set sigma value. None means tetrahedron method."""
        if sigma is None:
            self._sigma = None
        else:
            self._sigma = float(sigma)

    def set_grid_point(self, grid_point):
        """Set a grid point at which joint-DOS is calculated."""
        self._grid_point = grid_point
        self._set_triplets()
        if self._phonon_done is None:
            self._allocate_phonons()
        self._joint_dos = None
        self._frequency_points = None
        self._phonon_done[0] = 0
        self.run_phonon_solver(np.array([grid_point], dtype="int_"))

    def get_triplets_at_q(self):
        """Return triplets information."""
        return self._triplets_at_q, self._weights_at_q

    @property
    def bz_grid(self) -> BZGrid:
        """Return BZGrid."""
        return self._bz_grid

    def run_phonon_solver(self, grid_points):
        """Calculate phonons at grid_points.

        This method is used in get_triplets_integration_weights by this
        method name. So this name is not allowed to change.

        """
        run_phonon_solver_c(
            self._dm,
            self._frequencies,
            self._eigenvectors,
            self._phonon_done,
            grid_points,
            self._bz_grid.addresses,
            self._bz_grid.QDinv,
            self._frequency_factor_to_THz,
            self._nac_q_direction,
            self._lapack_zheev_uplo,
        )

    def _run_c(self, lang="C"):
        if self._sigma is None:
            if lang == "C":
                self._run_c_with_g()
            else:
                if self._temperatures is not None:
                    print(
                        "JDOS with phonon occupation numbers doesn't work "
                        "in this option."
                    )
                self._run_py_tetrahedron_method()
        else:
            self._run_c_with_g()

    def _run_c_with_g(self):
        self.run_phonon_solver(self._triplets_at_q.ravel())
        max_phonon_freq = np.max(self._frequencies)
        self._frequency_points = get_frequency_points(
            max_phonon_freq=max_phonon_freq,
            sigmas=[
                self._sigma,
            ],
            frequency_points=None,
            frequency_step=self._frequency_step,
            num_frequency_points=self._num_frequency_points,
        )
        num_freq_points = len(self._frequency_points)

        if self._temperatures is None:
            jdos = np.zeros((num_freq_points, 2), dtype="double")
        else:
            num_temps = len(self._temperatures)
            jdos = np.zeros((num_temps, num_freq_points, 2), dtype="double")
            occ_phonons = []
            for t in self._temperatures:
                freqs = self._frequencies[self._triplets_at_q[:, 1:]]
                occ_phonons.append(
                    np.where(freqs > self._cutoff_frequency, bose_einstein(freqs, t), 0)
                )

        for i, freq_point in enumerate(self._frequency_points):
            g, _ = get_triplets_integration_weights(
                self,
                np.array([freq_point], dtype="double"),
                self._sigma,
                is_collision_matrix=True,
                neighboring_phonons=(i == 0),
            )

            if self._temperatures is None:
                jdos[i, 1] = np.sum(
                    np.tensordot(g[0, :, 0], self._weights_at_q, axes=(0, 0))
                )
                gx = g[2] - g[0]
                jdos[i, 0] = np.sum(
                    np.tensordot(gx[:, 0], self._weights_at_q, axes=(0, 0))
                )
            else:
                for j, n in enumerate(occ_phonons):
                    for k, l in list(np.ndindex(g.shape[3:])):
                        jdos[j, i, 1] += np.dot(
                            (n[:, 0, k] + n[:, 1, l] + 1) * g[0, :, 0, k, l],
                            self._weights_at_q,
                        )
                        jdos[j, i, 0] += np.dot(
                            (n[:, 0, k] - n[:, 1, l]) * g[1, :, 0, k, l],
                            self._weights_at_q,
                        )

        self._joint_dos = jdos / np.prod(self._bz_grid.D_diag)

    def _run_py_tetrahedron_method(self):
        thm = TetrahedronMethod(self._bz_grid.microzone_lattice)
        self._vertices = get_tetrahedra_vertices(
            np.array(
                np.dot(thm.get_tetrahedra(), self._bz_grid.P.T), dtype="int_", order="C"
            ),
            self._bz_grid.D_diag,
            self._triplets_at_q,
            self._bz_grid,
        )
        self.run_phonon_solver(self._vertices.ravel())
        f_max = np.max(self._frequencies) * 2
        f_max *= 1.005
        f_min = 0
        self._set_uniform_frequency_points(f_min, f_max)

        num_freq_points = len(self._frequency_points)
        jdos = np.zeros((num_freq_points, 2), dtype="double")
        for vertices, w in zip(self._vertices, self._weights_at_q):
            for i, j in list(np.ndindex(self._num_band, self._num_band)):
                f1 = self._frequencies[vertices[0], i]
                f2 = self._frequencies[vertices[1], j]
                thm.set_tetrahedra_omegas(f1 + f2)
                thm.run(self._frequency_points)
                iw = thm.get_integration_weight()
                jdos[:, 1] += iw * w

                thm.set_tetrahedra_omegas(f1 - f2)
                thm.run(self._frequency_points)
                iw = thm.get_integration_weight()
                jdos[:, 0] += iw * w

                thm.set_tetrahedra_omegas(-f1 + f2)
                thm.run(self._frequency_points)
                iw = thm.get_integration_weight()
                jdos[:, 0] += iw * w

        self._joint_dos = jdos / np.prod(self._bz_grid.D_diag)

    def _init_dynamical_matrix(self):
        self._dm = get_dynamical_matrix(
            self._fc2,
            self._supercell,
            self._primitive,
            nac_params=self._nac_params,
            frequency_scale_factor=self._frequency_scale_factor,
            symprec=self._symprec,
        )

    def _set_triplets(self):
        if not self._is_mesh_symmetry:
            if self._log_level:
                print("Triplets at q without considering symmetry")
                sys.stdout.flush()

            (self._triplets_at_q, self._weights_at_q, _, _) = get_nosym_triplets_at_q(
                self._grid_point, self._bz_grid
            )
        else:
            (self._triplets_at_q, self._weights_at_q, _, _) = get_triplets_at_q(
                self._grid_point, self._bz_grid
            )

    def _allocate_phonons(self):
        num_grid = len(self._bz_grid.addresses)
        num_band = self._num_band
        self._phonon_done = np.zeros(num_grid, dtype="byte")
        self._frequencies = np.zeros((num_grid, num_band), dtype="double")
        itemsize = self._frequencies.itemsize
        self._eigenvectors = np.zeros(
            (num_grid, num_band, num_band), dtype=("c%d" % (itemsize * 2))
        )
