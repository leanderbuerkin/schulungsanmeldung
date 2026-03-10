# Schlungsanmeldung

This repository provides Python code to assign humans (by priorities and rules) to events.
It is used by the JDAV BaWü to determine the participants per Schulung.

This repository defines a standard with tests and debugging functions
so that everybody can easily create and verify new algorithms.
It also contains some algorithms to solve the problem.

## Usage

All commands are only tried on Linux Mint.
So feel free to contribute the commands for other operating systems.

### Optional: Create a Virtual Python Environment

```bash
python3 -m venv .venv 
```

### Install All Needed Packages

Remove the part before the `&` if you don't use a virtual python environment.

```bash
source .venv/bin/activate & pip install -r requirements.txt
```

## Contribute

### Save All Needed Packages

```bash
pip freeze > requirements.txt
```

## ToDos

Get all datafields of JuLeis and Schulungen from Teams
