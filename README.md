# mockup

Mock-up *dummy* model to build the experiment system


## Build docker
```
docker build -t {user}/mockup .
```

## Run docker and create forecast
```
docker run --rm --volume {model_path}/mockup/:/usr/src/mockup:rw {user}/mockup python run.py
```



