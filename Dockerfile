# pymock image for floatCSEP (build: docker)
# floatCSEP runs the image CMD as the host user, with the window input folder mounted
# at /app/input (args.txt, catalog.csv) and the forecasts folder at /app/forecasts
FROM python:3.12-slim

WORKDIR /app
COPY pyproject.toml setup.cfg ./
COPY pymock ./pymock
RUN pip install --no-cache-dir .

ENV MPLCONFIGDIR=/tmp
CMD ["pymock", "/app/input/args.txt", "/app/forecasts"]
