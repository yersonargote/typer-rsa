import base64
from typing import List, Optional

import typer

from algo import decrypt, encrypt, generateKeys, loadKeys, sign, verify

app = typer.Typer()


@app.command()
def keys():
    """
    Generate public and private keys.
    """
    generateKeys()


@app.command()
def save(
        user: str = typer.Option(..., help="Use: --user user"),
        passw: str = typer.Option(..., help="Use: --passw password")
        ):
    """
    Save the user and password given.
    """
    typer.echo(f"{user}:{passw}")
    try:
        public, _ = loadKeys()
        hash: bytes = encrypt(passw, public)
        pass_hash = base64.b64encode(hash).decode()
        with open("saved/passwords.txt", "a") as f:
            f.write(f"{user}:{pass_hash}")
            typer.echo(f"User: {user}\nPassword: {pass_hash} saved")
    except FileNotFoundError as e:
        typer.echo(f"Error: {e}")


def saved(user: str) -> Optional[str]:
    """
    Say if user hash password saved.
    """
    with open("saved/passwords.txt", "r") as f:
        line: str
        for line in f:
            parts: List[str] = line.split(":")
            if parts[0] == user:
                return parts[1]
        return None


@app.command()
def get(user: str = typer.Option(..., help="Use: --user user")):
    """
    Get a password given a hash.
    """
    hash: Optional[str] = saved(user)
    if hash is None:
        typer.echo(f"User {user} no has a password saved.")
        return
    pass_hash = base64.b64decode(hash.encode())
    if(hash is None):
        typer.echo("Not password saved.")
        return
    try:
        private, _ = loadKeys()
        passw = decrypt(pass_hash, private)
        typer.echo(f"Password: {passw}.")
    except FileNotFoundError:
        typer.echo("Try first the option keys.")


@app.command()
def valid(passw: str = typer.Option(..., help="Use: --passw password")):
    """
    Say if password is valid.
    """
    try:
        public, private = loadKeys()
        signature = sign(passw, private)
        if(verify(message=passw, signature=signature, key=public)):
            typer.echo("Correct password")
        else:
            typer.echo("Incorrect password")
    except FileNotFoundError:
        typer.echo("Try first the keys option.")


if __name__ == "__main__":
    app()
