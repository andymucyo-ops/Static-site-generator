#!/bin/bash

uv run main.py
cd public && uv run -m http.server 8888
