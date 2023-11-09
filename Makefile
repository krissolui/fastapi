SHELL=/bin/bash

dev:
	uvicorn app.main:app --reload

start:
	uvicorn app.main:app