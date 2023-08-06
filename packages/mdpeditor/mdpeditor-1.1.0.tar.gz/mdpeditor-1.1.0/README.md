# MDP Editor

Easily produce molecular dynamics simulation parameter input for
[GROMACS](https://gitlab.com/gromacs/gromacs).

- say it with words
  - compile pre-defined `.mdp` input parameter blocks reflecting best practices
  for different simulation scenarios
- script parameter file generation and alteration
  - swap parameter blocks when, e.g., simulating with a different force-field
- document the intent of your parameter settings
  - written `.mdp` files store the command that was used to generate them,
  simplifying documentation of simulation run input
- simple input files
  - write only the parameters that you need

## Features

- [x] stable command line interface
- [x] parameter blocks for the most common simulation scenarios
- [x] documentation of pre-defined parameter blocks on the command line
- [x] manually setting specific parameters
- [x] providing and updating own `.mdp` files
- [x] option to write minimal output
- [ ] addition of more complex parameter blocks
  - [x] density guided simulations
  - [ ] free energy calculation scenarios
  - [ ] QM/MM
- [x] parameter evaluation (like `nsteps` from setting `simulation-time-in-ns`)
- [x] textual user interface
- [ ] graphical user interface
- [x] help text for parameters
- [ ] `grompp` parameter check

## Examples

Compile the pre-defined block `force_field.charmm` and sets `nsteps = 100` in the output

```bash
mdpeditor compile force_field.charmm nsteps=100
```

yields

```bash
dt              = 0.002
nsteps          = 100
coulombtype     = PME
rcoulomb        = 1.2
vdw-modifier    = Force-switch
rvdw            = 1.2
dispcorr        = no
fourierspacing  = 0.15
constraints     = h-bonds
```

Write only values that were set when compiling `pressure.atmospheric` with
`force_field.charmm`, skip all defaults

```bash
mdpeditor compile pressure.atmospheric force_field.charmm
```

Show the available pre-defined parameter blocks

```bash
mdpeditor compile help
```

Learn more about a certain parameter block

```bash
mdpeditor explain density_guided.vanilla
```

Add atomspheric pressure coupling to a user-defined .mdp file, discarding all
non-GROMACS entries in `user.mdp`.

```bash
mdpeditor compile user.mdp pressure.atmospheric
```

Describe the `integrator` parameter

```bash
mdpeditor explain integrator
```

## Contributing

You can contribute by [opening a new issue](https://gitlab.com/cblau/mdpeditor/-/issues/new).

### Contributing or changing parameter blocks

Adding a new `.mdp` file in a subdirectory of `mdpeditor/mdpblocks` will add a
new block that is automatically discovered by the python package. The block of
commented first lines (using `;`) will be printed as description of the block.

Note that once you built an executable as described above, the parameter blocks
are packaged with the executable and cannot be changed.

## Installing and running

Install the latest release from the python package manager

```bash
pip3 install mdpeditor
```

Then run it

```bash
mdpeditor
```

## Installing and running from source (if you must)

Running directly from the shell

```bash
./mdp-editor.py
```

### Installation with pip

We use `setuptools` with a `setup.cfg` and `pyproject.toml` file.

To build a distribution from the source directory install

```bash
pip3 install build
```

Then run this in the source directory to build the distribution on your system

```bash
python3 -m build
```

Eventually, find the build in `dist/` and install the `.tar.gz` file found
there with

```bash
pip install dist/mdpeditor*.tar.gz
```

Make sure to install the right `.tar.gz` if you ran the build command
multiple times.

### Generating a single executable

To generate a single executable that you can run almost anywhere run

```bash
pip3 install pyinstaller
pyinstaller --onefile mdpeditor.spec
```

You will find the executable in

```bash
dist/
```

## Author

Christian Blau
