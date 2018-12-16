FROM python:3.7
MAINTAINER Machserve "admin@machserve.io"
COPY . /mach_prerelease
WORKDIR /mach_prerelease
ENV PIPENV_DONT_LOAD_ENV=1
ENV PORT=8080
RUN pip install pipenv
RUN pipenv run pip install -e .
RUN pipenv install --system --deploy
CMD ["python", "entrypoint.py"]
