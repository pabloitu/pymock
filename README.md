# mockup

Mock-up *dummy* model to build the experiment system


## Docker build

```
docker build \
--build-arg USERNAME=$USER \
--build-arg USER_UID=$(id -u) \
--build-arg USER_GID=$(id -g) \
--no-cache \
-t mockup .
```

## Docker run

```
docker run --rm --volume $PWD:/usr/src/mockup:rw mockup python run.py
```


