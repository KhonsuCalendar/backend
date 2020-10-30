FROM python:3.8
ENV PATH="/root/.poetry/bin:${PATH}"
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py --output get-poetry.py
RUN python get-poetry.py --version 1.0.10 -y
RUN poetry config virtualenvs.create false
ADD pyproject.toml .
ADD poetry.lock .
RUN mkdir lunar_api
ADD lunar_api/__init__.py lunar_api
RUN poetry install
ADD . .
ENTRYPOINT poetry run python lunar_api/main.py