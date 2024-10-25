FROM python:3.10

RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

#WORKDIR /app

#COPY --chown=user . $HOME/app

COPY ./requirements.txt requirements.txt

#COPY --chown=user ./requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

#CMD ["chainlit", "run", "app.py", "--port", "7860"]
CMD ["chainlit", "run", "app.py", "--host=0.0.0.0", "--port", "8000"]

#CMD ["chainlit", "run", "app.py", "--port", "8000"]