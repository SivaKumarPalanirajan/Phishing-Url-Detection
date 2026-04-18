FROM python:3.10-slim
WORKDIR /app 
COPY requirements.txt .
COPY app.py .
COPY src/pipelines/PredictionPipeline.py src/pipelines/
COPY src/utils/common.py src/utils/
COPY artifacts-prediction/ artifacts-prediction/
RUN pip install -r requirements.txt
CMD ["streamlit","run","app.py","--server.address=0.0.0.0","--server.port=8501"]