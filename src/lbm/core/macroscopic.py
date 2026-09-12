import torch
from torch import Tensor
from lbm.models.lattice import Lattice

def macroscopic(f: Tensor, lattice: Lattice, force: Tensor = None) -> tuple[Tensor, Tensor, Tensor]:
    """
    Compute macroscopic density and velocity from distribution function f.
    
    Inputs:
    - f: (Ny, Nx, Q) distribution function
    - lattice_model: LatticeModel object
    
    Returns:
    - rho: (Ny, Nx)
    - u:  (Ny, Nx, 2) represting [ux, uy]
    """
    # Sum over directions to get density
    rho = f.sum(dim=-1)  # (Ny, Nx)

    # Extract velocity components
    cx = lattice.c[:,0].float().to(f.device)  # (Q,)
    cy = lattice.c[:,1].float().to(f.device)  # (Q,)

    # if force is not provided, set to zero
    if force is None:
        force = torch.zeros((*rho.shape, 2), dtype=f.dtype, device=f.device)  # (Ny, Nx, 2)

    # Compute momentum: sum_i f_i * c_i
    ux = ((f * cx.view(1,1,-1)).sum(dim=-1) + 0.5 * force[...,0]) / rho  # (Ny, Nx)
    uy = ((f * cy.view(1,1,-1)).sum(dim=-1) + 0.5 * force[...,1]) / rho  # (Ny, Nx)

    return rho, torch.stack([ux, uy], dim=-1) # return rho, and u