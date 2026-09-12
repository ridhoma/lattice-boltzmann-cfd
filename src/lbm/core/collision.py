import torch
from torch import Tensor
from lbm.models.lattice import Lattice

def collision_bgk(
        f: Tensor, 
        feq: Tensor, 
        tau: Tensor,
        force: Tensor = None,
        lattice: Lattice = None,
        rho: Tensor = None,
        u: Tensor = None
    ) -> Tensor:
    """
    Collision step: Move from current equilibrium state feq to the next f.
    Single Relaxation Time (SRT) model from Bhatnagar-Gross-Krook (BGK) equation.
    
    Inputs:
    - f: (Ny, Nx, Q) pre-collision distribution
    - f_eq: (Ny, Nx, Q) equlibrium distribution
    - tau: relaxation time
    - force: (Ny, Nx, 2) body force, optional default to None. If provided, Guo forcing scheme will be applied. 
    - lattice: models.lattice.Lattice object, optional default to None. Required if force is provided.
    
    Returns:
    - f_star: (Ny, Nx, Q) post-collision distribution
    """
    
    f_star = f - (1/(tau + 0.5)) * (f - feq)
    if force is not None:
        # apply Guo forcing scheme if force is provided
        if lattice is None:
            raise ValueError("lattice must be provided when force is not None")
        f_star += guo_force(f, force, lattice, tau, rho, u)
    return f_star
    

def guo_force(
        f: Tensor, 
        force: Tensor,
        lattice: Lattice,
        tau: Tensor,
        rho: Tensor,
        u: Tensor
    ) -> Tensor:
    """
    Guo forcing scheme to include body force in the collision step.
    
    Inputs:
    - f: (Ny, Nx, Q) distribution function
    - force: (Ny, Nx, 2) body force
    - lattice: models.lattice.Lattice object, e.g. D2Q9()
    - tau: relaxation time
    
    Returns:
    - S_i: (Ny, Nx, Q) Source term to be added to the post-collision distribution
    """
    theta = lattice.theta
    c = lattice.c          # (Q, 2)
    w = lattice.w          # (Q,)

    # (c_i - u) · F / theta
    ci_minus_u = c[None, None, :, :] - u[..., None, :]    # (Ny, Nx, Q, 2)
    term1 = torch.sum(ci_minus_u * force[..., None, :], dim=-1) / theta  # (Ny, Nx, Q)

    # (c_i · u)(c_i · F) / theta^2
    ci_dot_u = torch.einsum('qa,xya->xyq', c, u)          # (Ny, Nx, Q)
    ci_dot_F = torch.einsum('qa,xya->xyq', c, force)      # (Ny, Nx, Q)
    term2 = (ci_dot_u * ci_dot_F) / (theta ** 2)

    # weight each direction
    force_term = w[None, None, :] * (term1 + term2)       # (Ny, Nx, Q)

    # prefactor for trapezoidal BGK
    S_i = (1 - 0.5 / (tau + 0.5)) * force_term

    return S_i
