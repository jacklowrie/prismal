# Prismal

Opinionated scaffolding for AI/ML Research.

## Opinionated Choices

This is a summary of the key choices made by using this template.

### Project Organization

We base the project structure from the following perspective:

- experiments should be modular and composable
- all unnecessary print statements, but especially debug prints, are a nuisance
  when trying to write modular code.
- Data needs to follow consistent and expected schema in order for it to be
  readily passed between them
- each component of an experiment should be well-documented, both for
  collaborators and for downstream consumers of the research.
- notebooks are for analysis of data and results, not running experiments:
    - scripts beat notebooks for developing composable, reusable pipelines.
    - notebooks beat scripts for exploring, analyzing, and presenting data
      (inputs or results)

### Main Tech Stack

- `uv` for project/dependency management
- `pydantic` for config and data Schema
- `loguru` for more concise logging/debugging
These are the biggest opinionated choices, and the hardest ones to change - it
would be better to not use the template if these choices are unacceptable. We
make heavy use of [Astral](https://astral.sh)'s tooling in place of `conda`,
`mypy` (or no type annotations) and similar. `uv` only works with python
environments, but it excels at managing fully reproducable envs. It is also
highly performant in resolving and installing dependencies. Conda is great with
system dependencies, but not as much with reproducible python environments, and
system dependencies tend to be less portable. `conda` and `uv` can be used
together, so long as they aren't both trying to override each other. We opt here
to use uv, leaving system-specific configuration management to conda running on
the machines in question (since they will need to change each time). In short:
python dependencies get managed with `uv`, the rest (if necessary) is up to you.

We use `pydantic` to enforce consistent schema for experiment parameters
(configs like "models to test", "batch size", "temperature", etc), and for data
(including prompt datasets, response datasets, and results datasets). This both
makes it easier to find where key experiment variables are set, and to ensure
that data is stored as expected by each part of the experimental pipeline.

#### Dev Dependencies

- `prek` for automatic code checking on commits
- `pytest` for testing, though tests are not enabled in pre-commit hooks by
  default.
- `pdoc` for frictionless documentation generation.
- `ruff` for linting and formatting, with a fairly strict default ruleset.

We install `ty` and `prek` by default, and enforce type annotations. these help
ensure good coding practices and avoid major blocks (for example, needing to
"clean up the whole codebase" before publishing, or before merging when time is
short). We also install `pdoc`, for lightweight, zero-config documentation.
Sphinx is more powerful, but a nuisance if the docs are not regularly
referenced. `pytest` for optional test code. _is_ installed by default, however
test coverage is not set up, nor are tests part of `prek` by default. This is
because research code is often not a "product", so regression tests are
(debatably) less valuable. If you or someone on your team prefers tests for
their code (or practices TDD), they can with zero friction. We opt not to
incorporate them in common workflows to allow individuals to use their preferred
workflow. Finally, we use `ruff` to enforce a fairly comprehensive set of
linting rules by default. This can be customized as needed, however it's much
easier to start with a strict set of linting rules and relax than it is to add
linting rules after development is under way. Consider sticking with them -
they're meant to help researchers write code that is easier for future
researchers to understand, consume, reproduce, and expand on. `ruff` also
enforces code to be documented, making collaboration and publication easier.

We also add two core dependencies for convenience:

- `tqdm` for progress bars in notebooks and scripts - invaluable if you haven't
  used before.
- `dotenv` for secret management - especially great if using huggingface models

### Data analysis

These are easier to change, but we choose defaults with intention:

- `parquet` for data storage
- `polars` for dataframes
- `marimo` for notebooks

`parquet` is more performant than `csv` files, and `polars`/ and `marimo` are
more performant than their counterparts (`pandas` and `jupyter`). We use them by
default, however we leave toggles for switching or adding `pandas`/`jupyterlab`
if necessary. In order for research to scale to larger datasets, `polars` is
strongly encouraged.

### AI/ML

We use `PyTorch` and huggingface `transformers` by default for local work. If
training or local inference aren't necessary, these can be skipped. We also add
`accelerate` and `bitsandbytes` to help speed up inference on smaller/consumer
machines.

## Repo Structure

### Top-level directories

Research code and artifacts are organized with the following directory
structure:

- `colab/`: notebooks specifically meant for running experiments on colab.
- `configs/`: Experiment and model configuration files.
- `data/`: Canonical, version-controlled experiment inputs.
- `hpc/`: submission scripts for HPC clusters (i.e. SLURM jobs).
- `notebooks/`: Jupyter/Marimo notebooks for analysis and exploration.
- `outputs/`: Canonical, version-controlled experiment outputs.
- `scripts/`: Runnable entry points for experiments/pipelines.
- `src/`: Reusable experiment code (rename for your project).
- `tests/`: Automated tests.
Consider adding READMEs to configs/data/notebooks/outputs if these become
complex.

### Special Files

Additionally, there are some project/environment files to be aware of:

#### Python Configuration

- `.python-version`: Project Python version (managed by `uv`).
- `pyproject.toml`: Main project config. contains metadata, direct dependencies
  (managed by `uv`), and tool configurations.
- `uv.lock`: Lockfile with fully resolved, exact versions for all dependencies
  (managed by `uv`).

#### Repo/Environment config

- `.env.example`: Template of required environment variables (copy to `.env` for
  local secrets).
- `.gitignore`: project-specific ignores (local env ignores like .DS_Store go in
  your global .gitignore)
- `AGENTS.md`: Repository-specific agent/developer workflow guidelines.
- `prek.toml`: config for pre-commit automation (essentially, running the QA
  pipeline locally).

#### Bootstrapping

We provide two scripts that automate local setup, based on how you intend to use
the repo:

- `bootstrap.sh` bootstraps the env for conducting research (including dev
  dependencies etc)
- `bootstrap-run.sh` bootstraps the env for running/reproducing experiments
  already committed to the repo (skips dev-specific steps).

## Installation

This is a template repository. It can be used by either downloading the source
code to init a fresh repository, or by clicking "use this template" from the
repository on [GitHub](https://github.com/jacklowrie/prismal).

### Using the template

You can create a template directly from this repo on GitHub (easier/preferred),
or by copying all of the files into your own repo. Either way, make sure to
update the following in your copy of the template:

1. Replace project metadata in `pyproject.toml` with your own project metadata.
2. Rename the root package name for your source code
   (`mv src/prismal src/[your_project]`)
3. Remove any commented/unnecessary dependency groups and linter rules
   `from pyproject.toml`
4. remove all tests from `tests`
5. UPDATE this README with your own project specifics, and remove the
   "Opinionated Choices" section and this section of the installation
   instructions.

### Setting up local env

1. Clone or download this repo.
2. Install `uv`:
   - on mac/linux, you can install with [homebrew](https://brew.sh/):
     `brew install uv`
   - on windows, you can install with
     [winget](https://winstall.app/apps/astral-sh.uv):
     `winget install --id=astral-sh.uv`
   - You can also use their standalone installer:
        - `curl -LsSf https://astral.sh/uv/install.sh | sh`
        - `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
   - See [the docs](https://docs.astral.sh/uv/) for alternative methods.
3. Install the project:
   - `uv sync --frozen` for a standard install
   - `uv sync --frozen --no-dev` to run code

### Additional dependencies

Depending on your use-case, you may need to additionally install dependency
groups from `pyproject.toml`:

- `uv sync --frozen --group [group_name]`.
- to install all dependencies at once, you can use
  `uv sync --frozen --all-extras`. However, this is not recommended if you don't
  need to, especially in a metered environment.
