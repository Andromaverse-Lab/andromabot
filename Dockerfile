###
FROM python:3.10 as poetry_builder

ENV PATH="/root/.local/bin:$PATH"
ENV POETRY_VIRTUALENVS_CREATE=false

RUN curl -sSL https://install.python-poetry.org | python -

###
FROM poetry_builder as builder

# Install ImageMagick
RUN apt update \
    && apt install -y \
         imagemagick 

WORKDIR /andromabot
COPY cache/ cache/
COPY images/ images/

COPY dependencies/ dependencies/
COPY pyproject.toml .
RUN poetry lock \
    && poetry install --no-dev

COPY andromabot/ andromabot/

# Update this to copy your config file
# to the container and then tag the image
# you plan to deploy to Akash.
# COPY config.yaml config.yaml

ENTRYPOINT [ "python", "-m", "andromabot" ]
