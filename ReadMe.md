# Schlungsanmeldung

This repository provides Python code to assign humans (by priorities and rules) to events.
It is used by the JDAV BaWü to determine the JuLeis per Schulung.

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
