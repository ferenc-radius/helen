FROM python:3.11-slim-bookworm as python-base

ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_PATH=/opt/poetry \
    WORKDIR=/app \
    # Don't buffer `stdout`
    PYTHONUNBUFFERED=1 \
    # Don't create `.pyc` files
    PYTHONDONTWRITEBYTECODE=1 \
    USER=nonroot \
    GROUP=nonroot \
    UID=12345 \
    GID=23456 \
    HOME=${WORKDIR}

# --- build virtualenv with poetry ---
FROM python-base AS builder

WORKDIR /tmp
ADD pyproject.toml poetry.lock /tmp/

RUN pip install poetry \
    && poetry config virtualenvs.options.no-pip true \
    && poetry config virtualenvs.in-project true \
    && poetry install --no-ansi --no-interaction --without dev

# --- runtime image ---
FROM python-base as runtime

# Fix security vulns on build time with latest debian upgrades
# only done in runtime stage to improve build times
RUN apt-get update && apt-get upgrade -y --no-install-recommends \
    # pip not needed after this point, fixing #PRISMA-2022-0168
    && pip uninstall -y pip setuptools ensurepip \
    # Running Docker as root user is a security risk, so here we create a new (non-root) user to run the rest of the file as
    && adduser --disabled-password --gecos "" nonroot \
    # cleanup
    && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/ && rm -rf /var/cache \ 
    # remove unnecessary files
    && rm -rf /usr/share/doc && rm -rf /usr/local/include && rm -rf /var/lib/dpkg

# Use the virtualenv created in the builder stage
COPY --from=builder /tmp/.venv/ /opt/python
ENV PATH=/opt/python/bin:$PATH

# Add source code
WORKDIR ${WORKDIR}
ADD run.py ${WORKDIR}/run.py
ADD tracker ${WORKDIR}/tracker

# Give the nonroot user permissions for /app/
RUN chown -R nonroot:nonroot ${WORKDIR} \
    && chmod -R 777 ${WORKDIR}

USER nonroot

# Running Python Application
CMD ["python", "run.py"]