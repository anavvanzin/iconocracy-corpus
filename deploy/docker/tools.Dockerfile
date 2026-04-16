# tools — conda iconocracy env (Python 3.11, jupyter, schema validators, corpus scripts)
# Build context: repo root. Run: docker compose run --rm tools <cmd>
FROM mambaorg/micromamba:1.5

USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends git make ca-certificates && \
    rm -rf /var/lib/apt/lists/*

USER $MAMBA_USER
COPY --chown=$MAMBA_USER:$MAMBA_USER environment.yml /tmp/environment.yml
RUN micromamba env create -f /tmp/environment.yml && \
    micromamba clean --all --yes

ENV ENV_NAME=iconocracy
ARG MAMBA_DOCKERFILE_ACTIVATE=1

WORKDIR /workspace
CMD ["bash"]
