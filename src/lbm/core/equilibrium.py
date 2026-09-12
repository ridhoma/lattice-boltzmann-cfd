import torch
from torch import Tensor
from lbm.models.lattice import Lattice


def feq_2nd_order(
        rho: Tensor, 
        ux: Tensor, 
        uy: Tensor, 
        lattice: Lattice
    ) -> Tensor:
    """
    Compute equilibrium distribution function (f^{eq}_i) approximated to 2nd-order Taylor expansion about u=0
    
    Inputs:
    - rho: (Ny, Nx) density
    - ux, uy: (Ny, Nx) velocity components
    - w: (Q,) weights
    - c: (Q,2) discrete velocities
    - theta: cs^2 where cs^2 is lattice speed of sound squared
    
    Returns:
    - feq: (Ny, Nx, Q) equilibrium distributions
    """

    Ny, Nx = rho.shape
    Q = lattice.Q
    # shape (Q,1,1) for broadcasting over (Ny,Nx)
    cx = lattice.c[:,0].float().view(Q, 1, 1).to(rho.device)
    cy = lattice.c[:,1].float().view(Q, 1, 1).to(rho.device)
    w = lattice.w.view(Q, 1, 1).to(rho.device)
    theta = lattice.theta

    u_sq = ux**2 + uy**2 # (Ny, Nx)
    cu = cx*ux + cy*uy   # (Ny, Nx, Q)
    
    # equilibrium distribution # (Q, Ny, Nx)
    feq = w * rho.unsqueeze(0) * (
        1 + cu/theta + 0.5*(cu**2)/(theta**2) - 0.5*(u_sq)/theta
    )                    
    
    # permute to (Ny, Nx, Q)
    feq = feq.permute(1, 2, 0).contiguous()
    
    return feq