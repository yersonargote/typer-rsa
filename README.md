# First Typer App

CLI to save user:password information, password is hashed by rsa.

## Setup

### Virtualenv
```bash
python3 -m venv venv

source ./venv/bin/activate
```

### Install modules

```bash
pip install -r requirements.txt
```

## Use

### Generate keys

```bash
python3 main.py keys
```

### Save user and password

```bash
python3 main.py save --user user --passw password
```

### Get the password given the user

```bash
python3 main.py get --user user
```
