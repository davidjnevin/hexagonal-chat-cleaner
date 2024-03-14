FROM python:3.11
LABEL name=chat-cleaner-app \
	  version=0.1.0 \
	  maintainer="David J Nevin"

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY requirements.txt /tmp/requirements.txt
COPY requirements-dev.txt /tmp/requirements-dev.txt

RUN set -ex ;\
	apt-get update -y ; \
	apt-get install -y --no-install-recommends gettext ;\
	pip install --no-cache-dir --upgrade pip ;\
	pip install --no-cache-dir --upgrade -r /tmp/requirements-dev.txt ;\
	useradd -U app_user ;\
	install -d -m 0755 -o app_user -g app_user /app/static ;\
	rm -rf \
		/var/lib/apt/lists/*

WORKDIR /app
USER app_user:app_user

COPY --chown=app_user:app_user . .
USER root
RUN chmod 755 /app/entrypoint.sh

ENTRYPOINT [ "/app/entrypoint.sh" ]
CMD ["server"]
