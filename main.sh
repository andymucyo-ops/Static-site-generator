#!/bin/bash

uv run main.py
cd docs && uv run -m http.server 8888
