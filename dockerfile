FROM python:3.9-slim

# 1. Install corporate certificates (if needed)
ARG CORPORATE_CERT_URL=""
RUN if [ -n "$CORPORATE_CERT_URL" ]; then \
    apt-get update && \
    apt-get install -y ca-certificates curl && \
    curl -k -o /usr/local/share/ca-certificates/corporate-cert.crt "$CORPORATE_CERT_URL" && \
    update-ca-certificates && \
    apt-get purge -y curl && \
    apt-get autoremove -y; \
    fi

# 2. Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    tesseract-ocr \
    tesseract-ocr-fra && \
    rm -rf /var/lib/apt/lists/*

# 3. Configure pip to trust hosts
RUN pip config set global.trusted-host "pypi.org files.pythonhosted.org pypi.tuna.tsinghua.edu.cn"

# 4. Set working directory and copy files
WORKDIR /app
COPY ./app/requirements.txt .
RUN pip install --no-cache-dir --trusted-host pypi.org -r requirements.txt
COPY ./app .

# 5. Environment variables
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata

# 6. Run the application
EXPOSE 8501
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]