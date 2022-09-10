#!/bin/bash
set -e
alembic revision --autogenerate -m "$(date +%Y-%m-%d-%H%M)"
