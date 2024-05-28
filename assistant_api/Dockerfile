FROM python:3.10-bullseye

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    libssl-dev \
    adduser \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    LANG=C.UTF-8 \
    APP_HOME=/src/api \
    NLTK_DATA=/usr/local/share/nltk_data

WORKDIR $APP_HOME

ARG GID=1000
ARG UID=1000
ARG USER=user_api
RUN groupadd --gid $GID $USER \
    && useradd --uid $UID --gid $GID $USER \
    && echo "$USER:$USER" | chpasswd

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip poetry

COPY --chown=$USER:$USER ./pyproject.toml pyproject.toml

RUN poetry export -f requirements.txt --output requirements.txt
RUN pip install -r requirements.txt --no-cache-dir
RUN pip install torch==2.2.2 torchvision==0.17.2 torchaudio==2.2.2 --index https://download.pytorch.org/whl/cpu


COPY --chown=$USER:$USER ./src $APP_HOME
RUN python -m nltk.downloader punkt -d $APP_HOME

USER $USER

ENTRYPOINT ["gunicorn", "main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000"]