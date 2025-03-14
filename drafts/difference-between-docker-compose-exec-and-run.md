# The Difference Between `docker compose exec` and `docker compose run`

In the past, I've used the commands `docker compose exec [some container] bash` and
`docker compose run [some container] bash` pretty much interchangeably. I figured there was some
subtle, probably unimportant, difference between them. Recently I learned what it is.

Recently I had a problem where I ran the `run` variant to check the contents of a configuration file
and to my surprise it was missing entirely! I suspected this `exec`/`run` business to be the culprit
so I tried using `exec` instead and sure enough the missing configuration file was there.

As it turns out, `docker compose exec [some container] [command]` will run the given command in
the docker container that is already running. On the other hand, 
`docker compose run [some container] [command]` spins up a fresh container.

But how does that explain the missing configuration file? In our case we have a `Dockerfile` that's
laid out kind of like this:

```dockerfile
FROM ubuntu:latest as base

WORKDIR /app
# ... Do a bunch of things ...

FROM base as development

# ... Do a bunch of extra things ...
# Build all the configuration files:
CMD ./entrypoint.sh
```

Then we have a `docker-compose.yml` that looks like this:

```yaml
# ...
services:
    app:
        build:
            context: .
            target: development
# ...
```

With this setup, when I ran docker compose up, it would build the container with the `development`
target and the configuration files would be created. Then when I ran `docker compose exec app bash`,
I'd see the files. However when I ran `docker compose run app bash`, it would make a new container
that was built with the `base` target which didn't have the files!

If you're like me, even after learning this you'll have some trouble recalling
which command is which, so here's a silly mnemonic to help:

* (ex)ec is for (ex)isting containers
* (r)u(n) is for (r)unning a (n)ew container

I'm still not exactly clear why the `run` command doesn't just build the new container
with the `development` target but I'll update this TIL if I figure it out.