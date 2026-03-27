default:
  just --list

run *args:
  poetry run uvicorn src.main:app --reload {{args}}

mm *args:
  poetry run alembic revision --autogenerate -m "{{args}}"

migrate:
  poetry run alembic upgrade head

downgrade *args:
  poetry run alembic downgrade {{args}}

ruff *args:
  poetry run ruff check {{args}} src

lint:
  poetry run ruff format src
  just ruff --fix

# grpc
gen-proto:
  #!/usr/bin/env bash
  set -e
  for proto_file in $(find src -name "*.proto"); do
    dir=$(dirname "$proto_file")
    poetry run python -m grpc_tools.protoc \
      -I "$dir" \
      --python_out="$dir" \
      --grpc_python_out="$dir" \
      "$proto_file"
    grpc_file="${proto_file%.proto}_pb2_grpc.py"
    sed -i '' 's/^import \(.*_pb2\)/from . import \1/' "$grpc_file"
    echo "Generated stubs for $proto_file"
  done

# docker
up:
  docker-compose up -d

kill *args:
  docker-compose kill {{args}}

build:
  docker-compose build

ps:
  docker-compose ps