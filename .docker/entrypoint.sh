#!/bin/sh

# exec so the Python process becomes PID 1 and receives signals directly
# (graceful shutdown on SIGTERM from Kubernetes).
exec python -m src.main
