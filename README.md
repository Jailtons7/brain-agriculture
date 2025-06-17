# BRAIN AGRICULTURE
Brain Agriculture is an application to manage crops and harvests on rural properties

---

## Dependencies
 - docker (tested on version 28.2.2)
 - docker compose (tested on version 2.36.2)
 - GNU Make (optional)

---

## Running
First of all, copy the `src/.env.example` file content to a `src/.env` file.
Then build the project
```shell
  make build
```

execute the migrations and create a superuser:
```shell
  make migrations
```

```shell
  make createsuperuser
```

and finally, run the local server:
```shell
  make runserver
```

If you don't have <strong>GNU Make</strong> installed, you can simply execute the
respective command written in the `Makefile`.

---
## Testing

This project has automated tests, to run them execute

```shell
  make test
```

You can also test it manually in the Django Administration Site `/admin` or using the docs `/redoc`.
