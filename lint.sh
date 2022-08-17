#!/usr/bin/env bash

poetry run isort andromabot tests
poetry run black andromabot tests
poetry run flake8 andromabot tests
