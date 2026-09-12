# 2. Lattice Boltzmann Method

LBM takes a discretisation of the velocity vector $\mathbf{v} = \{\mathbf{c}_0, \mathbf{c}_1, ..., \mathbf{c}_i\}$. Under discrete velocity vector, the equilibrium velocity distribution function becomes;
$$
\begin{equation}
f^\text{eq}_i(\mathbf{x}, t) = \rho w_i \left[ 
    1 
    + \frac{\mathbf{c}_i \cdot \mathbf{u}}{\theta} 
    + \frac{1}{2} \left( \frac{\mathbf{c}_i \cdot \mathbf{u}}{\theta} \right)^2
    + \frac{u^2}{2\theta} 
    \right]
\end{equation}
$$

The parameters $w_i$ amnd $\theta$ in discretised model must be chosen to satisfy the moment-matching equations;

$$
\begin{align}
\sum_i w_i = 1 \rightarrow \sum_i f^{\text{eq}}_i = \rho &\quad \text{conservation of mass} \\
\sum_i w_i c_{i\alpha} = 0 \rightarrow \sum_i f^{\text{eq}}_i \mathbf{c}_i = \rho \mathbf{u} &\quad \text{conservation of momentum} \\
\sum_i w_i c_{i\alpha} c_{i\beta} = \theta \delta_{\alpha \beta} \rightarrow \sum_i f^{\text{eq}}_i c_{i\alpha} c_{i\beta} = \rho(\theta \delta_{\alpha\beta} + u_{\alpha} u_{\beta}) &\quad \text{isotropic pressure tensor}\\
\end{align}
$$

## Isotropic Pressure Tensor and Equation of State

From the Boltzmann viewpoint, the pressure tensor (or stress tensor) is the second velocity moment of the distribution function.
$$
\begin{align}
\Pi^{\text{eq}}_{\alpha\beta} &= \sum_i f^{\text{eq}}_i c_{i\alpha} c_{i\beta} \\
    &= \rho(\theta \delta_{\alpha\beta} + u_{\alpha} u_{\beta})
\end{align}
$$

The isotropic condition means that when the value of $\mathbf{u}=0$ (no drift velocity), the pressure tensor has to be the same in all direction. Mathematically $\Pi^{\text{eq}}_{\alpha\beta} = p\delta_{\alpha\beta}$, a pressure/stress tensor/matrix where the diagonals are $p$ and the other elements are $0$. Plugging in we got the **equation of state** (relationship between macroscopic variables):

$$
\begin{equation}
p = \rho\theta
\end{equation}
$$

In isothermic case, constant $\theta$, this means pressure $p$ equals to density $\rho$ scaled by $\theta$. The value of $\theta$ in lattice unit can be derived from the second moment of the distribution function;

$$
\begin{align}
\sum_i w_i |\mathbf{c}_i|^2 &= \sum_{\alpha}\sum_i w_i c_{i\alpha}c_{i\alpha} =  \sum_{\alpha} \theta \delta_{\alpha\alpha} = D\theta \\
\theta &= \frac{1}{D} \sum_i w_i |\mathbf{c}_i|^2
\end{align}
$$
where $D$ is the number of dimension in the computational simulation. For example in 2D domain with D2Q9 velocity discretisation model, $\theta = 1/3$ (discussed later)

## Boltzmann Transport Equation under Discretisation of Velocity  

Assume no body force $\mathbf{F}=0$ (for simplicity, will hanlde later separately), the BTE under velocity discretisation becomes:

$$
\begin{equation}
\partial_t f_i(\mathbf{x}, t) + \mathbf{c}_i \cdot \nabla_x f_i(\mathbf{x}, t) = - \frac{1}{\tau} \left[ f_i(\mathbf{x}, t) - f^\text{eq}_i(\mathbf{x}, t) \right]
\end{equation}
$$

The LHS (streaming process) is equal to total time derivative $df_i/dt$, so we can rewrite in discrete form;
$$
\begin{equation}
\frac{f_i(\mathbf{x} + \mathbf{c}_i \Delta t, t + \Delta t) - f_i(\mathbf{x}, t)}{\Delta t} = - \frac{1}{\tau} \left[ f_i(\mathbf{x}, t) - f^\text{eq}_i(\mathbf{x}, t) \right]
\end{equation}
$$

This has equivalently integral form from $t$ to $t + \Delta t$. Since in lattice unit we can define $\Delta t = 1$, then we can write;

$$
\begin{equation}
f_i(\mathbf{x} + \mathbf{c}_i \Delta t, t + \Delta t) - f_i(\mathbf{x}, t) = - \frac{1}{\tau} \int_{t}^{t + 1} \left[ f_i(\mathbf{x}, t) - f^\text{eq}_i(\mathbf{x}, t) \right] dt
\end{equation}
$$

## Standard LBM: Euler Integration—1st Order Accuracy in time
$$
\begin{equation}
    \int_{t}^{t + 1} \left[ f_i(\mathbf{x}, t) - f^\text{eq}_i(\mathbf{x}, t) \right] dt 
    \approx 
    \left[ f_i(\mathbf{x}, t) - f^\text{eq}_i(\mathbf{x}, t) \right]
\end{equation}
$$

Plugging in and rearrange, we got the Lattice Boltzmann time-step update equation that gives a 1st order accuracy in time

$$
\begin{equation}
    f_i(\mathbf{x} + \mathbf{c}_i, t + 1) 
    = 
    f_i(\mathbf{x}, t) - \frac{1}{\tau} \left[ f_i(\mathbf{x}, t) - f^\text{eq}_i(\mathbf{x}, t) \right]
\end{equation}
$$

## More accuracy: Trapezoidal Integration—2nd Order Accuracy in time
Simplyfying the expression $f_i(\mathbf{x}, t) = f_i$ and $f^\text{eq}_i(\mathbf{x}, t) = f^{\text{eq}}_i$

$$
\begin{equation}
    \int_{t}^{t + 1} \left[ f_i - f^\text{eq}_i \right] dt 
        \approx \frac{1}{2} \left[ 
            \left(f_i - f^\text{eq}_i\right)|_t 
            + \left(f_i - f^\text{eq}_i\right)|_{t+1} 
        \right]
\end{equation}
$$

Plugging in we get;

$$
\begin{equation}
    f_i(\mathbf{x} + \mathbf{c}_i t, t + 1) = 
        f_i(\mathbf{x}, t) 
        - \frac{1}{2 \tau} \left[ 
            \left(f_i - f^\text{eq}_i\right)|_t 
            + \left(f_i - f^\text{eq}_i\right)|_{t+1} 
        \right]
\end{equation}
$$

This is an implicit equation since the RHS contains the unknown $t + 1$. To make equation explicit (thus solveable), introduce a modified distribution $\tilde{f}_i$ defined as;
$$
\begin{equation}
\tilde{f}_i = f_i - \frac{1}{2\tau}\left[f_i - f^\text{eq}_i \right]
\end{equation}
$$

After some algebra, we can have explicit time-step update function for $\tilde{f}_i$ and this is 2nd-order accuracy in time;

$$
\begin{equation}
    \tilde{f}_i(\mathbf{x} + \mathbf{c}_i, t + 1) 
    = 
    \tilde{f}_i(\mathbf{x}, t) - \frac{1}{\tau + 1/2} \left[ 
        \tilde{f}_i(\mathbf{x}, t) - f^\text{eq}_i(\mathbf{x}, t) 
    \right]
\end{equation}
$$

**An interesthing property**; 
> It can be derived (Ask ChatGPT) that the modified ditribution $\tilde{f}$ recover the same conservations as the original distribution $f$. So there is no practical need to transform $\tilde{f}$ back to $f$. In other words, the trapesoidal integration method is just Euler method with relaxation time shifted by $1/2$ in lattice unit
> $$
\tau_{\text{trapezoid}} = \tau_{\text{Euler}} + 1/2 \quad \text{in lattice unit, } \Delta t = 1
$$

## Computational Implementation

### A. Streaming and Collision Steps

Lattice Boltzmann Method usually solve the equation of dynamics by separating the equation above into 2 steps: Streaming and Collision. Procedurally, solving the LBM is as follows;

**Initialisation**

Initialise $f_i(\mathbf{x}, 0), t=0$. If using trapezoidal, calculate $\tilde{f}_i = f_i - \left[f_i - f^{\text{eq}}_i \right]/(2\tau)$

A common simple initialisation is chosing $f_i = \tilde{f}_i = f^{\text{eq}}_i$

**Loop over time**
1. Compute macroscopic quantities from $\tilde{f}_i (\mathbf{x}, t)$, yielding $\rho(\mathbf{x}, t)$ and $\mathbf{u}(\mathbf{x}, t)$, visualise
2. Compute equilibrium distribution $f^{\text{eq}}_i (\mathbf{x}, t)$
3. Collision step:
   $$
   \tilde{f}^{*}_i(\mathbf{x}, t) = 
   \tilde{f}_i(\mathbf{x}, t)
   - \frac{1}{\tau + 1/2} \left[ \tilde{f}_i(\mathbf{x}, t) - f^\text{eq}_i(\mathbf{x}, t) \right]
   $$
4. Streaming step:
   $$
   \tilde{f}^{*}_i(\mathbf{x}, t) \rightarrow \tilde{f}_i(\mathbf{x} + \mathbf{c}_i, t + 1)
   $$
5. Apply boundary condition (Bounce back on walls/obstacles, Zou-He, etc.). Most of boundary condition implementations can be operated directly on $\tilde{f}$ without having to reconstruct $f$
6. Repeat ...

## Lattice to Physical Unit Conversion

### Viscosity and Relaxation Time Relation

Suppose a physical space with length $L$ is to be simulated in a latticice with square cells with resolution $\Delta x = L/N_x$. $ \Delta t = \tau_{\text{phys}} / \tau_{\text{lattice}}$ represents a time equivalent between 1 timestep in lattice unit and in physical unit.

Relationship between viscosity $\nu$ and relaxation time $\tau$ depends on the time resolution and discretisation method. If using 2nd-order trapezoidal integration;
$$
\nu = \theta \left(\tau - \frac{\Delta t}{2} \right)
$$
Above equation is valid in physical and lattice unit. In lattice unit, as $\Delta t=1$, stability requires a lattice simulation design where $\tau_{\text{lattice}} > 1/2$ so that $\nu > 0$. With $\theta$ equal to speed of sound (need to explain);
$$
\theta_{\text{phys}} = c^2_{s\text{,phys}} 
= \left( \frac{\Delta x}{\Delta t} \right)^2 c^2_{s\text{,lattice}}
= \left( \frac{\Delta x}{\Delta t} \right)^2 \theta
$$

we can calculate $\tau_{\text{lattice}}$ (or let's just call it $\tau$) as;
$$
\tau_{\text{phys}} = 
    \frac{\Delta t}{2} 
    + \frac{\nu_{\text{phys}} \Delta t^2}{\theta \Delta x^2}
$$
and since $ \Delta t = \tau_{\text{phys}} / \tau_{\text{lattice}}$ , we can rewrite;
$$
\tau_{\text{lattice}} \equiv \tau =
    \frac{1}{2} 
    + \frac{\nu_{\text{phys}} \Delta t}{\theta \Delta x^2}
$$
Not only viscosity constraint, there's also Mach constraint because LBM only valid at low Mach number $\text{Ma} = u_{\text{lattice}}/c_{s,\text{lattice}} \ll 1$. So we need to keep the lattice veolocity small;
$$
u_{\text{lattice}} = \frac{u_{\text{phys}} \Delta t}{\Delta x} \lesssim 0.1
\Rightarrow \Delta t \lesssim 0.1 \frac{\Delta x}{u_{\text{phys}}}
$$

So here we got a framework to design our lsattice. With LBM, we can only simulate physical system with low speed (low Mach number) that translates to lattice speed of about $u_{\text{lattice}} \approx 0.1$ for practical purpose. Then we can set $\Delta x$ that gives $\Delta t$ a value that will make $\tau > 1/2$. Stability best practice is to design $\tau \in [0.55, 1]$.