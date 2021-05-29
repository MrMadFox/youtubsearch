FROM python:3.9-slim as build
WORKDIR /app
RUN pip install -q virtualenv
RUN virtualenv venv
COPY ./api/req.txt .
RUN venv/bin/pip install --no-cache-dir -q -r req.txt && rm req.txt
ENV PYTHONPATH=/app/src:$PYTHONPATH

FROM python:alpine as prod

WORKDIR /app
COPY --from=build /app .
COPY ./api ./src
ENV PYTHONPATH=/app/src:$PYTHONPATH
CMD ["venv/bin/uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "8080", "--loop", "uvloop", "--http", "httptools"]