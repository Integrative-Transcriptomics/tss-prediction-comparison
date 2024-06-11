#!/bin/bash

source venv/Scripts/activate

venv/Scripts/python.exe -m flask --app app/server.py run
