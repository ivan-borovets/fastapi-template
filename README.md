# README TEMPLATE

```
config.toml }- Makefile (local/docker?)       # these two to configure
     |            |
     v            v
settings.py <-- .env --> docker-compose.yaml  # these three to autogenerate
          \              /
           \            /
            \  ✨🚀✨  /
              database                        # for this one to be accessible 
       (the same parameters of
        connection & creation)
```

**Pretty much all** you need to do is fill out `config.toml` and run the command from `Makefile`. 
Even `alembic.ini` and `alembic/env.py` can be configured this way.

What to do on your own:
- Examine `$ make help`
- Add and review the settings (in `config.toml`)
- Write the project code... (in `src/` & `tests/`)

> I just want to run this template ASAP!

Ok. Then run 
```sh
make compose.up.new
```
And check out http://0.0.0.0:8000/docs

To stop the containers run
```sh
make compose.down
```

To be filled out soon...
