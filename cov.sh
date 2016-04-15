#!/usr/bin/env bash

py.test --cov-report html --cov=morenines && open htmlcov/index.html
