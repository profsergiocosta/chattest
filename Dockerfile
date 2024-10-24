FROM python:3.10
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

RUN pip install --no-cache-dir --upgrade pip

COPY --chown=user . $HOME/app

COPY --chown=user ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt


COPY . .
CMD ["chainlit", "run", "app.py", "--host", "0.0.0.0","--port", "7860"]