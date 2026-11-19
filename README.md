# microlensing_mpd_interpolator

> **Status: work in progress.** This is an unfinished project. The notebooks
> are exploratory and the pipeline is not yet consolidated into reusable code.
> Some notebooks and scripts reference absolute paths to data on other
> machines (e.g. `/home/favio/software/microlensing/`, `/fred/oz108/...`,
> `/mnt/d/data/...`) and will not run as-is elsewhere.

Tools for computing and interpolating the microlensing mass probability
distribution (MPD) for point-mass lenses with a macro-model (convergence
$\kappa$, shear $\gamma$), including systems with binary ("double") lenses.

The workflow:
1. Generate light curves with **GERLUMPH** (`lsst_generator`) on a grid of
   macro-model parameters $(\kappa, \gamma, s)$.
1. Build a uniform 4-D grid of MPDs (in $\log_{10}\mu$) from the simulated
   magnification histograms.
3. Interpolate from the grid to obtain the MPD for arbitrary parameter values.

## Directory layout

| Path | Description |
|---|---|
| `microlensing_mpd/` | Python package with the interpolation code (`utils.py`, `get_mpd.py`, `compare_mpd.py`) and pre-computed grid data. |
| `ozstar/` | SLURM job scripts for running GERLUMPH simulations on a cluster. |
| `*.ipynb` | Jupyter notebooks covering each stage of the workflow (see below). |
| `bayesian_microlensing/` | Clone of [weisluke/bayesian_microlensing](https://github.com/weisluke/bayesian_microlensing) for comparison. **Not tracked** in this repo. |

## Notebooks

| Notebook | Purpose |
|---|---|
| `masterlist_to_db.ipynb` | Import the master list of lens maps into a SQLite database. |
| `generate_input_cpp.ipynb` | Generate `input_cpp.json` files for GERLUMPH runs. |
| `create_bash_slurm.ipynb` | Create SLURM batch scripts for cluster submission. |
| `mpd.ipynb` | Compute MPDs from simulated magnification histograms. |
| `check_convolved_mpds.ipynb` | Inspect and validate convolved MPD results. |
| `create_uniform_grid_mpd.ipynb` | Build the uniform 4-D MPD grid (with inpainting for missing cells). |
| `interpolate_mpd_from_uniform.ipynb` | Interpolate the MPD from the uniform grid. |
| `Interpolate_mpd_nonuniform_grid.ipynb` | Alternative interpolation on a non-uniform grid. |
| `interpolator_vs_luke.ipynb` | Compare interpolated MPDs with Bayesian microlensing results. |
| `plot_gerlumph_mpd.ipynb` | Plot GERLUMPH-derived MPDs. |
| `source_sizes_in_RE_mosquera11.ipynb` | Source size distributions (Mosquera et al. 2011). |

## Requirements

- Python 3 with: `numpy`, `scipy`, `matplotlib`, `pandas`, `scikit-image`, `astropy`
- [GERLUMPH / lsst_generator](../lsst_generator/) for light-curve simulation
- SQLite (bundled with Python)

## Usage

### Interpolating an MPD

```bash
cd microlensing_mpd
python get_mpd.py <kappa> <gamma> <s>
# e.g. python get_mpd.py 0.3 0.2 50
```

This loads the pre-computed grid from `data/mpd_grid_inpaint.npy` and returns
the MPD in $\log_{10}\mu$ (relative to the macro-model magnification) via
nearest-neighbour interpolation (`scipy.ndimage.map_coordinates`).

### Comparing with Bayesian results

```bash
cd microlensing_mpd
python compare_mpd.py
```

Compares interpolated MPDs against histograms from `bayesian_microlensing/data/histograms/`
and runs a Kolmogorov–Smirnov test.

### Running GERLUMPH simulations (cluster)

The `ozstar/` directory contains SLURM scripts. Each job runs
`micro_mag_hist` from `lsst_generator` on a specific map:

```bash
sbatch ozstar/imf_doubles_mpd_job_00.sh
```

## Data files

| File | Description |
|---|---|
| `microlensing_mpd/data/mpd_grid.npy` | Raw 4-D MPD grid (2.6 GB). **Not tracked.** |
| `microlensing_mpd/data/mpd_grid_inpaint.npy` | Inpainted 4-D MPD grid (2.6 GB). **Not tracked.** |
| `microlensing_mpd/kappa_list.txt` | Grid values for $\kappa$ (step 0.01). |
| `microlensing_mpd/gamma_list.txt` | Grid values for $\gamma$ (step 0.01). |
| `microlensing_mpd/s_list.txt` | Grid values for source size $s$ (in milliarcsec). |
| `microlensing_mpd/log10_mu.txt` | Bin centres for $\log_{10}\mu$ (400 bins). |
| `mapids.txt` | List of map IDs used in the simulations. |
| `input_cpp.json` | Example GERLUMPH input file. |

The large `.npy` grid files and generated figures are excluded from version
control (see `.gitignore`). Regenerate them with the notebooks above.
