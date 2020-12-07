FROM python:3.8
WORKDIR /app
COPY . .
RUN pip --no-cache-dir install -r requirements.txt
EXPOSE 8000
ENTRYPOINT ["python"]
CMD ["app.py"]