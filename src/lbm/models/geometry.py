import torch
from torch import Tensor

# lbm/core/geometry.py
import torch

def channel2D(Nx: int, Ny: int, walls: str) -> Tensor:
    """2D channel with walls at top and bottom."""
    if walls not in ("top_bottom", "left_right"):
        raise ValueError("walls must be 'top_bottom' or 'left_right'")
    obstacles = torch.zeros((Ny, Nx), dtype=torch.bool)
    if walls == "top_bottom":
        obstacles[0, :] = True
        obstacles[Ny-1, :] = True
    elif walls == "left_right":
        obstacles[:, 0] = True
        obstacles[:, Nx-1] = True
    return obstacles

def cavity2D(Nx: int, Ny: int) -> Tensor:
    """Square cavity with walls on all four sides."""
    obstacles = torch.zeros((Ny, Nx), dtype=torch.bool)
    obstacles[0, :] = True
    obstacles[Ny-1, :] = True
    obstacles[:, 0] = True
    obstacles[:, Nx-1] = True
    return obstacles

def cylinder2D(Nx: int, Ny: int, cx: int, cy: int, r: int) -> Tensor:
    """Circular obstacle inside the domain."""
    y, x = torch.meshgrid(torch.arange(Ny), torch.arange(Nx), indexing="ij")
    mask = (x - cx)**2 + (y - cy)**2 <= r**2
    return mask
