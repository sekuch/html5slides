#!/bin/bash

while [[ true ]]; do
	inotifywait -e modify slides.md
	python2 render.py
done
