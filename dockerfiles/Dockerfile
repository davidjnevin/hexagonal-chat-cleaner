FROM python:3.11
LABEL org.opencontainers.image.source=https://github.com/davidjnevin/hexagonal-chat-cleaner
LABEL org.opencontainers.image.description="A python/fastapi chat text cleaner"

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

ARG UID=1000
ARG GID=1000

COPY requirements.txt /tmp/requirements.txt
COPY requirements-dev.txt /tmp/requirements-dev.txt

# Install dependencies
RUN set -ex ;\
	apt-get update -y ; \
	apt-get install -y --no-install-recommends gettext ;\
	pip install --no-cache-dir --upgrade pip ;\
	pip install --no-cache-dir --upgrade -r /tmp/requirements-dev.txt

# Create a non-root user
RUN useradd -U app_user -u ${UID} -g ${GID}
RUN echo "app_user id is ${UID}"
RUN echo "app_user gid is ${GID}"

# Create a directory for static files
RUN install -d -m 0755 -o app_user -g app_user /app/static

WORKDIR /app
USER app_user:app_user

COPY --chown=app_user:app_user . .
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT [ "/app/entrypoint.sh" ]
CMD ["server"]
