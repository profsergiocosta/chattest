FROM python:3.10
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app



COPY --chown=user ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY --chown=user . $HOME/app
#CMD ["chainlit", "run", "app.py", "--port", "7860"]

EXPOSE 8000

CMD ["chainlit", "run", "app.py", "--port", "8000"]