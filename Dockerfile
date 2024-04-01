FROM python:3.12.2-alpine3.18 AS base

### Build the Ansible runtime
FROM base AS builder

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  PATH="$PATH:/runtime/bin" \
  PYTHONPATH="$PYTHONPATH:/runtime/lib/python3.12/site-packages" \
  # Versions:
  POETRY_VERSION=1.7.1

# System deps:
RUN apk add build-base unzip wget python3-dev libffi-dev
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /src

# Generate requirements and install *all* dependencies.
COPY pyproject.toml poetry.lock /src/
RUN poetry export --dev --without-hashes --no-interaction --no-ansi -f requirements.txt -o requirements.txt
RUN pip install --prefix=/runtime --force-reinstall -r requirements.txt

### Final container

FROM base AS runtime
COPY --from=builder /runtime /usr/local
COPY . /playbook
WORKDIR /playbook
ENV PATH="$PATH:/runtime/bin"

# Install git, roles and collections
RUN apk add git openssh-client make && ansible-galaxy role install -r requirements.yml --force && ansible-galaxy collection install -r requirements.yml --force

CMD [ "ansible-playbook", "--version" ]

# Labels.
LABEL maintainer="sysops@dimension.sh" \
    org.label-schema.schema-version="1.0" \
    org.label-schema.build-date=$BUILD_DATE \
    org.label-schema.vcs-ref=$VCS_REF \
    org.label-schema.name="dimension-sh/infra" \
    org.label-schema.description="Dimension Infrastructure playbooks in Docker" \
    org.label-schema.url="https://github.com/dimension-sh/infra" \
    org.label-schema.vcs-url="https://github.com/dimension-sh/infra" \
    org.label-schema.vendor="Dimension"
