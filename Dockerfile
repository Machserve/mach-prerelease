FROM python:3.7
MAINTAINER Machserve "admin@machserve.io"
COPY . /mach_prerelease
WORKDIR /mach_prerelease
ENV PIPENV_DONT_LOAD_ENV=1
ENV PORT=443
RUN pip install pipenv
RUN pipenv run pip install -e .
RUN pipenv install --system --deploy
EXPOSE 443
CMD ["python", "entrypoint.py"]
