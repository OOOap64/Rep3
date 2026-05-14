FROM python

LABEL version="1.0"
LABEL puplish="14.05.2026"

WORKDIR /Rep

COPY . 

RUN pip install flask Flask-JWT-Extended bcrypt

ENV PYTHONPATH=/Rep 
ENV DEBUG=1

EXPOSE 8000

CMD ['python', 'app.py']