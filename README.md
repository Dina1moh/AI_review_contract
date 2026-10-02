# Commercial Contract Review

An early-stage Python project for reviewing commercial contracts. Project setup and dependencies are defined in `pyproject.toml`, and the package source is under `src/application_contract_erview`.

> Run these steps in a **WSL / Ubuntu terminal**. A `.venv` created on Windows is separate from the WSL environment and is not used by these steps.

## Prerequisites

- Windows with WSL2 and an Ubuntu distribution.
- An internet connection.
- Enough disk space to download Miniconda and Python dependencies.

The project requires **Python 3.14 or newer**, as specified in `pyproject.toml` and `.python-version`.

## 1. Open the project in WSL

Open an Ubuntu/WSL terminal and go to the project directory:

```bash
cd /mnt/d/APPLICATION_CONTRACT_REVIEW
```

If your project is in a different location, replace this with its path inside WSL. The Windows `D:` drive is usually mounted at `/mnt/d`.

## 2. Install Miniconda in WSL

Run these commands in a WSL terminal, not PowerShell. They download the installer to your home directory, run it, and remove the installer after setup:

```bash
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh
bash ~/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda.sh
~/miniconda3/bin/conda init bash
```

Close and reopen the WSL terminal, or reload the Bash configuration in the current terminal:

```bash
source ~/.bashrc
```

Confirm that Conda is available:

```bash
conda --version
```

If you see `conda: command not found`, run `~/miniconda3/bin/conda init bash`, then close and reopen the terminal.

## 3. Create the project environment

From the project directory, create a Conda environment named `review_contract` with Python 3.14 and `uv`:

```bash
conda create -n review_contract -c conda-forge python=3.14 pip uv -y
conda activate review_contract
```

Verify that the terminal is using Python from the Conda environment:

```bash
python --version
which python
uv --version
```

`python --version` should report Python 3.14 or newer. The `which python` path should point to the `review_contract` environment under `~/miniconda3/envs/`.

## 4. Install the project and its dependencies

With `review_contract` activated, run this command from the project root:

```bash
uv pip install -e .
```

This installs the project in editable mode and reads its dependencies from `pyproject.toml`. You do not need to install `requirements.txt` as well; the current file does not include all dependencies declared for the project.

### 4.1. How to add a new package with uv

If you want to add a library to the project and keep it compatible with the versions declared in `pyproject.toml`, use `uv add` from the project root:

```bash
conda activate review_contract
uv add package-name
```

This updates the project metadata and installs the package into the active environment.

If you want to install dependencies from a `requirements.txt` file only into the current environment, use:

```bash
conda activate review_contract
uv pip install -r requirements.txt
```

The difference is important:

- `uv add package-name` -> updates the project dependency list in `pyproject.toml`
- `uv pip install -r requirements.txt` -> installs the listed packages into the active environment only

Verify the installation:

```bash
python -m pip list
```

## 5. Run the current entry point

The project is currently at an early stage. Its configured command prints a simple verification message:

```bash
application-contract-erview
```

Expected output:

```text
Hello from application-contract-erview!
```

## 6. Open the project in VS Code using WSL

From a WSL terminal in the project directory, run:

```bash
code .
```

In VS Code, select the Conda Python interpreter for `review_contract`. Its usual path is:

```text
/home/<your-wsl-username>/miniconda3/envs/review_contract/bin/python
```

To find the exact path after activating the environment, run:

```bash
which python
```

Make sure the VS Code window is connected to WSL. The Windows interpreter in `.venv` is not the WSL interpreter.

## Using the project later

Whenever you open a new WSL terminal:

```bash
cd /mnt/d/APPLICATION_CONTRACT_REVIEW
conda activate review_contract
```

To leave the environment:

```bash
deactivate
```

## Common issues

- **`conda: command not found`:** Run `~/miniconda3/bin/conda init bash`, then reopen the WSL terminal.
- **`pip: command not found` or `externally-managed-environment`:** Make sure `review_contract` is activated and `which python` points to `~/miniconda3/envs/review_contract/`. Do not install `python3-pip` with `apt` for this project or use `--break-system-packages`.
- **`uv: command not found`:** Activate the correct environment. If `uv` is not installed in it, run `conda install -n review_contract -c conda-forge uv`.
- **VS Code cannot see the installed packages:** Select the Conda interpreter in the WSL session, not the Windows interpreter or its `.venv`.
