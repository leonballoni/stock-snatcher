FROM python:3.12.7-slim-bullseye as builder

ENV POETRY_VIRTUALENVS_IN_PROJECT=true \
    USER="snatcher" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create a new user and set up locales
RUN useradd -m $USER \
    && apt-get update \
    && apt-get install --no-install-recommends -y \
        ca-certificates \
        locales \
    && locale-gen en_US.UTF-8 \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*

ENV LANG=en_US.UTF-8 \
    LANGUAGE=en_US:en \
    LC_ALL=en_US.UTF-8

# Set working directory
WORKDIR /home/$USER

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy the project files and set the correct ownership
COPY src/snatcher ./

COPY --chown=$USER:$USER . .

RUN poetry lock && poetry install

ENTRYPOINT ["sh", "./src/snatcher/boot.sh"]
