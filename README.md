# Prismal
Opinionated scaffolding for AI/ML Research.

## Project Structure
### Top-level directories
Research code and artifacts are organized with the following directory structure:
- `colab/`: notebooks specifically meant for running experiments on colab.
- `configs/`: Experiment and model configuration files.
- `data/`: Canonical, version-controlled experiment inputs.
- `hpc/`: submission scripts for HPC clusters (i.e. SLURM jobs).
- `notebooks/`: Jupyter/Marimo notebooks for analysis and exploration.
- `outputs/`: Canonical, version-controlled experiment outputs.
- `scripts/`: Runnable entry points for experiments/pipelines.
- `src/`: Reusable experiment code (rename for your project).
- `tests/`: Automated tests.
Consider adding READMEs to configs/data/notebooks/outputs if these become complex.

### Special Files
Additionally, there are some project/environment files to be aware of:

#### Python Configuration
- `.python-version`: Project Python version (managed by `uv`).
- `pyproject.toml`: Main project config. contains metadata, direct dependencies (managed by `uv`), and tool configurations.
- `uv.lock`: Lockfile with fully resolved, exact versions for all dependencies (managed by `uv`).

#### Repo/Environment config
- `.env.example`: Template of required environment variables (copy to `.env` for local secrets).
- `.gitignore`: project-specific ignores (local env ignores like .DS_Store go in your global .gitignore)
- `AGENTS.md`: Repository-specific agent/developer workflow guidelines.
- `prek.toml`: config for pre-commit automation (essentially, running the QA pipeline locally).

#### Bootstrapping
We provide two scripts that automate local setup, based on how you intend to use the repo:
- `bootstrap.sh` bootstraps the env for conducting research (including dev dependencies etc)
- `bootstrap-run.sh` bootstraps the env for running/reproducing experiments already committed to the repo (skips dev-specific steps).

## Installation
This is a template repository. It can be used by either downloading the source code to init a fresh repository,
or by clicking "use this template" from the repository on [GitHub](https://github.com/jacklowrie/prismal).

### Using the template
You can create a template directly from this repo on GitHub (easier/preferred), or by copying all of the files into your own repo. Either way, make sure to update the following in your copy of the template:
1. Replace project metadata in `pyproject.toml` with your own project metadata.
2. Rename the root package name for your source code (`mv src/prismal src/[your_project]`)
3. Remove any commented/unnecessary dependency groups and linter rules `from pyproject.toml`
3. UPDATE this README with your own project specifics, and remove this section of the installation instructions.

### Setting up local env
1. Clone or download this repo.
2. Install `uv`:
    - on mac/linux, you can install with [homebrew](https://brew.sh/): `brew install uv`
    - on windows, you can install with [winget](https://winstall.app/apps/astral-sh.uv): `winget install --id=astral-sh.uv`
    - You can also use their standalone installer:
        - `curl -LsSf https://astral.sh/uv/install.sh | sh`
        - `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
    - See [the docs](https://docs.astral.sh/uv/) for alternative methods.
3. Install the project:
    - `uv sync --frozen` for a standard install
    - `uv sync --frozen --no-dev` to run code

### Additional dependencies
Depending on your use-case, you may need to additionally install dependency groups from `pyproject.toml`:
- `uv sync --frozen --group [group_name]`.
- to install all dependencies at once, you can use `uv sync --frozen --all-extras`. However, this is not recommended if you don't need to, especially in a metered environment.
