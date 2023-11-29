FROM python:3.9.17-bullseye
WORKDIR /app

# Create virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Get dependencies
RUN apt update && apt install -y ffmpeg
RUN git clone https://github.com/yarrm80s/orpheusdl.git
RUN pip install -r orpheusdl/requirements.txt
RUN git clone https://github.com/uhwot/orpheusdl-deezer orpheusdl/modules/deezer
COPY settings.json /app/orpheusdl/config/settings.json
RUN pip install deezer-python
RUN pip install python-dotenv
RUN pip install yt-dlp

# Run
COPY . /app
CMD ["python3", "-u", "/app/autodownload.py"]