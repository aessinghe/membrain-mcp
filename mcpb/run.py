"""Entry point for the MCPB bundle.

A plain top-level script rather than pointing the bundle directly at
src/main.py: running "python src/main.py" makes Python treat src/ itself as
the script's directory and prepend it to sys.path, which does not reliably
resolve the package-relative imports inside main.py (`from src.config import
...`). Running this file from the project root instead lets the editable
install that `uv run` performs (via pyproject.toml) resolve the `src` package
normally, regardless of the host's exact invocation details.
"""

from src.main import main

if __name__ == "__main__":
    main()
