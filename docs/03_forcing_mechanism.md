# 3. BGK-LBM with Body Force

In Section 2 we have expressed the Boltzmann Transport Equation (BTE) in discretised velocity that makes the core principle of Lattice Boltzmann method. Trapezoidal integration is applied to derive the timestep update function with 2nd order accuracy in time. However, for simplicity, we derived it without including body force term by setting $\mathbf{F}=0$. Taking body force into account is not trivial because force term $\mathbf{F}$ appears in derivative _w.r.t._ velocities in the BTE. 
$$
\begin{equation}
    \partial_t f_{\mathbf{v}} + \mathbf{v} \cdot \nabla_{\mathbf{x}} f_{\mathbf{v}} + \frac{\mathbf{F}}{m} \cdot \nabla_{\mathbf{v}} f_{\mathbf{v}} = \Omega(f_{\mathbf{v}}, f^{\text{eq}}_{\mathbf{v}})
\end{equation}
$$

## Naive Forcing Mechanism (Euler Forward)

The simplest but naive way to incorporate body force into LBM equation is by using Euler forward method. Newton's law define force as change in momentum $\mathbf{F}(t) = d\mathbf{p}/dt$ which can be written in discrete form as;

$$
\begin{equation}
    \mathbf{F}(t)\Delta t = \rho\mathbf{u}|_{(t+\Delta t)} - \rho\mathbf{u}|_{(t)}
\end{equation}
$$

With $\Delta t=1$ in lattice unit and $ \rho\mathbf{u} = \sum_i \mathbf{c_i} f_i$, we can obtain the time-step update equation for momentum as:
$$
\begin{equation}
    \rho\mathbf{u}|_{(t+1)} = \sum_i \mathbf{c_i} f_i + \mathbf{F}
\end{equation}
$$

This this velocity update equation is accurate in time only to the 1st order. This is because the $f^{\text{eq}}$ calculated in the next step will use the forward time $\mathbf{u}^{(t+1)}$ and thus the next collision operator will operate on $f$ and $f^{\text{eq}}$ from different timestep, _i.e._ $\Omega(f^{(t)}, f^{\text{eq}(t+1)})$. This timestep missmatch cause an error known as **spurious velocity** (it's good if we can demonstrate it in an example notebook).

## Guo Forcing Mechanism

Guo, Zheng, and Shi in their paper titled _Discrete lattice effects on the forcing term in the lattice Boltzmann method_ published on Physical Review E in 2002 proposed that the macroscopic variables to be calculated at mid-point in time to recover 2nd-order accuracy in time for momentum update

$$
\begin{align}
    \text{Newton's law :}&\quad \mathbf{F}(t) = \rho\mathbf{u}|_{(t+1)} - \rho\mathbf{u}|_{(t)} \\
    \text{mid-point momentum :}&\quad\rho\mathbf{u}|_{(t+\frac{1}{2})} = \rho \mathbf{u}|_{(t)} + \frac{1}{2}\mathbf{F}(t)
\end{align}
$$

this leads to defining the macroscopic variable as;
$$
\begin{equation}
    \rho\mathbf{u} = \sum_i \mathbf{c}_i f_i + \frac{1}{2}\mathbf{F}
\end{equation}
$$

To complete the time step update before streaming—the next half of the time step—a source term $S_i$ is added to the collision step such that $\sum_i \mathbf{c}_i S_i = \mathbf{F}$. With this, the LBM equation becomes:

$$
\begin{equation}
    f_i(\mathbf{x} + \mathbf{c}_i, t + 1) - f_i(\mathbf{x}, t) 
    = - \frac{1}{\tau} \left[ 
        f_i(\mathbf{x}, t) - f^\text{eq}_i(\mathbf{x}, t) 
    \right]
    + S_i(\mathbf{x}, t)
\end{equation}
$$

The term $S_i$ must satisfy $\sum_i S_i = 0$ to maintain the conservation of mass. Guo _et.al._ then derived the expression for $S_i$ as; 
$$
\begin{equation}
S_i = \left(1 - \frac{1}{2\tau} \right) w_i \left[ 
    \frac{\mathbf{c}_i - \mathbf{u}}{\theta} 
    + \frac{(\mathbf{c}_i \cdot \mathbf{u})\mathbf{c}_i}{\theta^2}
\right] \cdot \mathbf{F}
\end{equation}
$$
It can be proven that the The prefactor $(1-\frac{1}{2\tau})$ and the $\frac{1}{2}F$ term ensure 2nd-order accuracy in time for the momentum evolution and remove the spurious velocity that appears in Euler forward mechanism **(\*learn the derivation later)**. Finally, while the 1st-moment equation (momentum conservation) changes with the addition of $+\frac{1}{2}F$ term, the 0th-moment (mass conservation) and 2nd-moment (pressure isotrophy) equations stay the same.