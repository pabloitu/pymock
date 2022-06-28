# mockup

Mock-up *dummy* model to build the experiment system


## Build docker
```
docker build -t {user}/mockup_py .
```

## Run docker and create forecast
```
docker run --rm --volume {model_path}/mockup_py/:/usr/src/mockup_py:rw {user}/mockup_py python run.py
```



