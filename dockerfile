FROM trickstermaster/neironkabbbot:template

WORKDIR /app

<<<<<<< HEAD
=======
COPY reqs.txt .

RUN pip install

>>>>>>> 39a12b3 (etcd test)
COPY . .

CMD ["python", "run.py"]
