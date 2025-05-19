FROM trickstermaster/neironkabbbot:template

WORKDIR /app

COPY . .

CMD ["python", "run.py"]
