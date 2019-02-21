# messenger-scripts
A collection of scripts to do random things in Facebook's Messenger chat (using carpedm20's FBChat API).

## Setup

1. Get pipenv and pyenv.
2. Run `pipenv install` in this directory
3. Run `pipenv run python antidelete.py setup` and follow the prompts
4. Run `pipenv run python antidelete.py` to start listening

## Customization

Edit `config.json` (made during setup).

### Passwords

Password parsing: No one likes plaintext passwords.
Therefore, there are two solutions: Python's builtin `getpass` module and `gnupg`. If you want to use `gnupg`, provide a path (the 'pass' key in `config.json`) to the encrypted file with your password. If you want to use `getpass`, leave it blank.

This only needs to be done once as an encrypted cookie file is generated automatically.

### Behavior

When the program is running, it checks whether a message is in a given thread or not.
Edit `config.json`'s 'threads' key which is a list for each thread it will check. If you leave it as an empty list, it will prompt you for a thread id.
