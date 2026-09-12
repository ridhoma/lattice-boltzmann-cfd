# 1. Maxwell-Boltzmann Statistics

An $\mathbb{R}^3 $ volume $V$ containing $N$ number of particles of mass $m$ has particle number density $n = N/V$. Number density of particles having velocity $\mathbf{v}$ under influence of drift/bulk velocity $\mathbf{u}$ follows Maxwell-Boltzmann distribution;

$$
\begin{equation}
f(\mathbf{v}) = n \left(\frac{m}{2\pi k_B T}\right)^{3/2} \exp\left(-\frac{m (\mathbf{v} - \mathbf{u})^2}{2 k_B T} \right)
\end{equation}
$$

Taking $k_B T / m = \theta$ and $f(\mathbf{v}) = f_{\mathbf{v}}$ we can rewrite above equation as;

$$
\begin{equation}
f_{\mathbf{v}} = n \left(2\pi \theta \right)^{-3/2} \exp \left(-\frac{(\mathbf{v} - \mathbf{u})^2}{2 \theta} \right)
\end{equation}
$$

It can be seen that $n$ is related to fluid density $\rho$ by relation $n = N/V = \rho N/m$. Because $N/m$ (number of particles per unit mass) is constant, we can say that $n \equiv \rho$ and either can be used interchangeably. $\rho$ being the more familiar quantity in fluid dynamics will be used from here on. 

Furthermore, with $v = |\mathbf{v}|$ and $u = |\mathbf{u}|$ we can calculate up to the 2nd moments of the distribution functions;
$$
\begin{align}
\int f_{\mathbf{v}} d^3 v &= \rho \\
\int \mathbf{v} f_{\mathbf{v}} d^3 v & = \rho \mathbf{u}\\
\int v^2 f_{\mathbf{v}} d^3 v & = \rho (u^2 + 3\theta) = \rho \varepsilon
\end{align}
$$

Notice that the 1st moment relates to mass density $\rho$, 2nd moment relates to drift/bulk velocity $\mathbf{u}$, and 3rd moment relates to energy density $\varepsilon$.

# 2nd Order Taylor Approximation 

Taking the 2nd-order taylor expansion about $u=0$ to approximate $f_v$:

$$
\begin{equation}
f_{\mathbf{v}} \approx f^0_{\mathbf{v}} \left[ 1 + \frac{\mathbf{v} \cdot \mathbf{u}}{\theta} + \frac{1}{2}\left(\frac{\mathbf{v} \cdot \mathbf{u}}{\theta}\right)^2 + \frac{u^2}{2\theta}\right] + \mathcal{O}(u^3)
\end{equation}
$$

where $f^0_{\mathbf{v}}$ is the equilibrium Maxwell-Boltzmann distribution with no bulk drift.

$$
\begin{equation}
f^0_{\mathbf{v}} = \rho \left(2\pi \theta \right)^{-3/2} \exp \left(-\frac{v^2}{2 \theta} \right)
\end{equation}
$$

Here we are saying: 
> _"Take the equilibrium Maxwell–Boltzmann distribution $f^0_{\mathbf{v}}$ with no bulk drift, then perturb it in powers of the bulk velocity $\mathbf{u}$"_

# Boltzmann Transport Equation (BTE)

Consider $f_{\mathbf{v}}=f(\mathbf{x}, \mathbf{v}, t)$, the equilibrium Maxwell-Boltzmann distribution may change over time via a collision process between particles described by a collision operator $\Omega(f_{\mathbf{v}})$
$$
\begin{align}
\frac{df_\mathbf{v}}{dt} &= \Omega(f_{\mathbf{v}}) \\
\partial_tf_\mathbf{v} 
    + \frac{d\mathbf{x}}{dt} \nabla_{\mathbf{x}} f_\mathbf{v}
    + \frac{d\mathbf{v}}{dt} \nabla_{\mathbf{v}} f_\mathbf{v}
    &= \Omega(f_{\mathbf{v}})
\end{align}
$$

$d\mathbf{x}/dt = \mathbf{v}$ is velocity, and $d\mathbf{v}/dt = \mathbf{F}/m$ is acceleration caused by body force $\mathbf{F}$. We can rewrite above equation as; 

$$
\begin{equation}
\partial_t f_{\mathbf{v}} + \mathbf{v} \cdot \nabla_{\mathbf{x}} f_{\mathbf{v}} + \frac{\mathbf{F}}{m} \cdot \nabla_{\mathbf{v}} f_{\mathbf{v}} = \Omega(f_{\mathbf{v}})
\end{equation}
$$

which is known as the **Botlzmann Transport Equation**. The LHS describes a "streaming" process and the RHS describes a "collision" process. The equation basically says that the flow of the distribution function depends on the collision process between particles in the system. One expression for the collision operator $\Omega(f)$ is known as Bathnagar-Gross-Krook (BGK) approximation:

$$
\begin{equation}
\Omega(f_{\mathbf{v}}) = \Omega(f_{\mathbf{v}}, f^{\text{eq}}_{\mathbf{v}}) = - \frac{1}{\tau}\left( f_{\mathbf{v}} - f^{\text{eq}}_{\mathbf{v}} \right)
\end{equation}
$$

where $\tau$ is statistical relaxation time, the mean transition time between one equilibrium state to the next. During this short period of time, the system is out of equilibrium with distribution function $f_{\mathbf{v}}$ before falling back to the new equilibrium distribution function $f^{\text{eq}}$ that is none other than the Maxwell-Boltzmann distribution function. This short duration transition is observed macroscopically as the viscosity.

