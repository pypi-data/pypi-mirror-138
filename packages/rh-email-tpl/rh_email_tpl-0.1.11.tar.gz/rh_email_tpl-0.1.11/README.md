# RegioHelden Email template

`rh_email_tpl` is a django app used to render RegioHelden styled HTML emails. It provides also multiple Django 
templatetags used as helpers for building HTML emails.

This project is meant to be used internally by RegioHelden organisation, as it has the company styles and logos.

## Installation

Simply run:
```
pip install rh_email_tpl
```

And add `rh_email_tpl` to your django `INSTALLED_APPS`. I.e.: in `settings.py` add:
```
INSTALLED_APPS = [
  ...
  "rh_email_tpl",
  ...
]
```

## Making a new release

[bumpversion](https://github.com/peritus/bumpversion) is used to manage releases.

Add your changes to the [CHANGELOG](./CHANGELOG.md) and run `bumpversion <major|minor|patch>`, then push (including tags)

## This project uses Black

We use the python [Black](https://black.readthedocs.io/en/stable/) code formatter.

If you would like to format code directly in your IDE, take a look [here](https://black.readthedocs.io/en/stable/editor_integration.html). This is possible in PyCharm, Sublime Text, VSCode ...

To ensure that your push will not be rejected, make sure to install [pre-commit](https://pre-commit.com/#install) on your machine.
Then inside the project folder run the following:
```sh
pre-commit install
```

This will install the required pre-commit hooks that will run everytime you will commit something.
For more details you can check the `.pre-commit-config.yaml` file
