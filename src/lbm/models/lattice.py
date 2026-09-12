from dataclasses import dataclass
import numpy as np
import torch

@dataclass(frozen=True)
class Lattice:
    name: str               # name of the lattice model
    D: int                  # number of dimensions
    Q: int                  # number of discrete velocities
    opposites: torch.Tensor # index of opposite directions
    w: torch.Tensor         # weights
    c: torch.Tensor         # discrete velocities
    theta: float            # lattice speed of sound squared

    def __repr__(self):
        return f"<Lattice {self.name}: dim={self.D}, q={self.Q}>"


def D2Q9() -> Lattice:
    name = "D2Q9"
    w = torch.tensor([4/9] + [1/9]*4 + [1/36]*4, dtype=torch.float32)
    c = torch.tensor([
            [0, 0], # 1 central
            [1, 0], [0, 1], [-1, 0], [0, -1], # 4 axial
            [1, 1], [-1, 1], [-1, -1], [1, -1] # 4 diagonal
        ], dtype=torch.float32
    )
    
    opposites = torch.tensor([0, 3, 4, 1, 2, 7, 8, 5, 6], dtype=torch.int64)
    theta = 1/3
    return Lattice(
        name=name,
        D=2, Q=9,
        w=w, c=c, 
        opposites=opposites, 
        theta=theta
    )


def D3Q19() -> Lattice:
    # Not yet validated. Do not use for now.
    name = "D3Q19"
    w = torch.tensor([1/3] + [1/18]*6 + [1/36]*12, dtype=torch.float32)
    c = torch.tensor(
        [[0, 0, 0],
        [1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1],
        [1, 1, 0], [-1, -1, 0], [1, -1, 0], [-1, 1, 0],
        [1, 0, 1], [-1, 0, -1], [1, 0, -1], [-1, 0, 1],
        [0, 1, 1], [0, -1, -1], [0, 1, -1], [0, -1, 1]], 
        dtype=torch.float32
    )
    opposites = torch.tensor([0, 2, 1, 4, 3, 6, 5,
                              8, 7, 10, 9,
                              12, 11, 14, 13,
                              16, 15, 18, 17], dtype=torch.int64)
    theta = 1/3
    return Lattice(
        name=name,
        D=3, Q=19,
        w=w, c=c,
        opposites=opposites,
        theta=theta
    )

