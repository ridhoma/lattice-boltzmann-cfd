import torch
from torch import Tensor
from lbm.models.lattice import Lattice

def streaming(
        f: Tensor, 
        lattice: Lattice
    ) -> Tensor:
    """
    Streaming step: propagate f_star along its discrete velocities.
    
    Inputs:
    - f: (Ny, Nx, Q) distribution at t to be streamed
    - lattice: Lattice object
    
    Returns:
    - f_next: (Ny, Nx, Q) distribution at (t + dt) after streaming
    """
    Ny, Nx, Q = f.shape
    f_next = torch.empty_like(f)
    
    # Get discrete velocities
    cx = lattice.c[:,0].int()
    cy = lattice.c[:,1].int()
    
    # Loop over directions (small, only Q iterations)
    for i in range(Q):
        f_next[:,:,i] = torch.roll(f[:,:,i], shifts=(cy[i], cx[i]), dims=(0,1))
    
    return f_next
