from dataclasses import dataclass
from lbm.models.lattice import Lattice
import numpy as np

@dataclass
class LatticeConfig:
    lattice: Lattice    # lattice model
    Nx: int             # number of lattice nodes in x direction    
    Ny: int             # number of lattice nodes in y direction
    dx: float           # lattice spacing
    dt: float           # time step
    tau: float          # relaxation time
    u: float            # lattice velocity (reduce Mach)
    rho: float = 1.0    # reference density in lattice units
    
    @property
    def Ma(self) -> float:
        # Mach number
        return self.u / np.sqrt(self.lattice.theta)
    
    @property
    def nu(self) -> float:
        # kinematic viscosity in lattice units
        return self.lattice.theta * self.tau 
    
    def __repr__(self):
        return f'''{self.__class__}:
            {self.lattice}
            dx: {self.dx} ({self.Ny} x {self.Nx}) grids (rows x cols)
            dt: {self.dt} s/step
            tau: {self.tau:.3f} (>0.55 for stability)
            Ma: {self.Ma:.3f} (<1.0 valid for incompressible system)
            nu_lattice: {self.nu:.3f} (>0.0 for stability)
        '''

@dataclass(frozen=True)
class PhysicalConfig:
    L: float         # domain length [m]
    W: float         # domain width [m]
    d: float         # characteristic length [m] (obstacle size, etc.)
    rho: float       # fluid density [kg/m^3]
    u: float         # characteristic velocity [m/s]
    mu: float        # dynamic viscosity [Pa.s]
    g: float         # gravity [m/s^2]

    @property
    def nu(self) -> float:
        return self.mu / self.rho   # kinematic viscosity

    @property
    def Re(self) -> float:
        return self.u * self.d / self.nu

    def __repr__(self):
        return f'''{self.__class__}:
            L: {self.L}, W: {self.W}, d: {self.d}
            Re: {self.Re:.2f}
            nu: {self.nu:.2f}
        '''


def make_lattice_config(
        phys: PhysicalConfig, 
        lattice: Lattice, 
        dx: float, 
        u_lattice: float
    ) -> LatticeConfig:

    Nx, Ny = int(np.ceil(phys.L/dx)), int(np.ceil(phys.W/dx))
    dt = u_lattice * dx / phys.u
    tau = 0.5 + phys.nu * dt / (lattice.theta * dx**2)
    return LatticeConfig(lattice=lattice, Nx=Nx, Ny=Ny, dx=dx, dt=dt, tau=tau, u=u_lattice)
