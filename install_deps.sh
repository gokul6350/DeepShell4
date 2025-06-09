#!/bin/bash
set -e

# Create site-packages directory
mkdir -p /app/lib/python3/site-packages

# Install base dependencies first
pip3 install --prefix=/app --no-index pip_cache/typing_extensions-4.14.0-py3-none-any.whl
pip3 install --prefix=/app --no-index pip_cache/idna-3.10-py3-none-any.whl
pip3 install --prefix=/app --no-index pip_cache/sniffio-1.3.1-py3-none-any.whl
pip3 install --prefix=/app --no-index pip_cache/anyio-4.9.0-py3-none-any.whl
pip3 install --prefix=/app --no-index pip_cache/h11-0.16.0-py3-none-any.whl
pip3 install --prefix=/app --no-index pip_cache/certifi-2025.4.26-py3-none-any.whl
pip3 install --prefix=/app --no-index pip_cache/httpcore-1.0.9-py3-none-any.whl
pip3 install --prefix=/app --no-index pip_cache/httpx-0.28.1-py3-none-any.whl
pip3 install --prefix=/app --no-index pip_cache/urllib3-2.4.0-py3-none-any.whl
pip3 install --prefix=/app --no-index pip_cache/charset_normalizer-3.4.2-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
pip3 install --prefix=/app --no-index pip_cache/requests-2.32.3-py3-none-any.whl
pip3 install --prefix=/app --no-index pip_cache/requests_toolbelt-1.0.0-py2.py3-none-any.whl
pip3 install --prefix=/app --no-index pip_cache/packaging-24.2-py3-none-any.whl
pip3 install --prefix=/app --no-index pip_cache/pyparsing-3.2.3-py3-none-any.whl
pip3 install --prefix=/app --no-index pip_cache/annotated_types-0.7.0-py3-none-any.whl
pip3 install --prefix=/app --no-index pip_cache/pydantic_core-2.33.2-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
pip3 install --prefix=/app --no-index pip_cache/typing_inspection-0.4.1-py3-none-any.whl
pip3 install --prefix=/app --no-index pip_cache/pydantic-2.11.5-py3-none-any.whl
pip3 install --prefix=/app --no-index pip_cache/orjson-3.10.18-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
pip3 install --prefix=/app --no-index pip_cache/zstandard-0.23.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
pip3 install --prefix=/app --no-index pip_cache/langsmith-0.3.45-py3-none-any.whl
pip3 install --prefix=/app --no-index pip_cache/langchain_core-0.3.64-py3-none-any.whl
pip3 install --prefix=/app --no-index pip_cache/langchain_google_genai-2.0.10-py3-none-any.whl
pip3 install --prefix=/app --no-index pip_cache/langchain_groq-0.3.2-py3-none-any.whl
pip3 install --prefix=/app --no-index pip_cache/google_ai_generativelanguage-0.6.15-py3-none-any.whl
pip3 install --prefix=/app --no-index pip_cache/google_generativeai-0.8.5-py3-none-any.whl
pip3 install --prefix=/app --no-index pip_cache/groq-0.26.0-py3-none-any.whl
pip3 install --prefix=/app --no-index pip_cache/PyYAML-6.0.2-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
pip3 install --prefix=/app --no-index pip_cache/rich-14.0.0-py3-none-any.whl
pip3 install --prefix=/app --no-index pip_cache/tqdm-4.67.1-py3-none-any.whl

# Install the main package
pip3 install --prefix=/app --no-index . 