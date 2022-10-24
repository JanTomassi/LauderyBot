FROM python:latest
ENV TOKEN=5135231411:AAH3pakFBnNi2lA05qvZePplz_uPasC0WPY

WORKDIR /NestLaundry

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT python3 src/main.py
