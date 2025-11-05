FROM python:3.12-slim

COPY . /app/

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["streamlit", "run", "predictiveModels.py", "&", "python", "bot.py"]

EXPOSE 8501