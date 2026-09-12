lbm-sim/
│
├── pyproject.toml        # or setup.py (if packaging with Poetry/pip)
├── README.md             # project overview + usage examples
├── requirements.txt      # dependencies (if not using Poetry)
│
├── src/                  # all your simulation source code lives here
│   └── lbm/              # package namespace
│       ├── __init__.py
│       │
│       ├── core/         # essential building blocks
│       │   ├── lattice.py        # defines lattice sets (D2Q9, D3Q19, etc.)
│       │   ├── collision.py      # BGK, MRT, trapezoidal, etc.
│       │   ├── streaming.py      # streaming step implementations
│       │   ├── forcing.py        # external force terms
│       │   └── utils.py          # helper functions
│       │
│       ├── bc/           # boundary conditions
│       │   ├── bounce_back.py
│       │   ├── zou_he.py
│       │   └── ...
│       │
│       ├── solver/       # solver orchestrator
│       │   ├── time_loop.py      # main timestep loop
│       │   ├── initialization.py
│       │   └── io.py             # saving/loading results
│       │
│       ├── models/       # “high-level” physics configurations
│       │   ├── lid_driven_cavity.py
│       │   ├── poiseuille_flow.py
│       │   └── ...
│       │
│       └── visualization/
│           ├── plot2d.py
│           ├── plot3d.py
│           └── diagnostics.py
│
├── examples/             # reproducible example scripts/notebooks
│   ├── cavity_flow.ipynb
│   ├── channel_flow.py
│   └── ...
│
├── tests/                # unit tests
│   ├── test_collision.py
│   ├── test_bc.py
│   └── ...
│
└── docs/                 # documentation (optional, Sphinx/MkDocs)
