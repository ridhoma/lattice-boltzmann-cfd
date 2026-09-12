import torch
from torch import Tensor
from lbm.models.lattice import Lattice

def bounce_back_on_obstacles(
        f: Tensor, 
        f_star: Tensor, 
        obstacles: Tensor, 
        lattice: Lattice) -> Tensor:
    """
    General bounce-back on obstacle locations.

    Inputs:
    - f: (Ny, Nx, Q) distribution function after streaming
    - f_star: (Ny, Nx, Q) distribution function before streaming
    - obstacle: (Ny, Nx) boolean mask (True where obstacle is present)
    - lattice_model: contains .opposites (Q,) array

    Updates f in-place.
    """

    # Bounce-back: replace distributions at obstacle nodes
    f[obstacles] = f_star[obstacles][:, lattice.opposites]

    return f