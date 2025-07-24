FROM demisto/fastapi:0.116.1.4266494

WORKDIR /api

COPY main.py .

COPY templates/ ./templates

RUN pip install "fastapi[standard]"

CMD ["fastapi", "run", "main.py", "--port", "80"]