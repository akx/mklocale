# mklocale

A small utility to download and combine translations.

## Configuration

Mklocale is configured with YAML files.

This example is useful for Django projects, where you'd need fresher
translations than are shipped with the project(s) themselves.

This would gather Finnish translations from the Transifex and Django projects
and meld them into `.po`/`.mo` files in the place expected by Django's machinery.

```yaml
target:
  - locale/{lang}/LC_MESSAGES/django.po
  - locale/{lang}/LC_MESSAGES/django.mo
transifex:
  - project: wagtail
    languages: fi
  - project: django
    languages: fi
```

## Invocation

If you expect to be using Transifex, make sure to set `TRANSIFEX_AUTH` to
your Transifex `user:password` string.  This is necessary because Transifex
does not support any sort of other authentication nor unauthenticated access
to projects.

Then simply run

```shell
$ python -m mklocale my_config.yaml
```

and things will happen.
