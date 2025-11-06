#!/usr/bin/env bash
set -e
: "${PORT:=8080}"
exec uvicorn app.api.main:app --host 0.0.0.0 --port "${PORT}"
