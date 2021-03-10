FROM ubuntu
RUN apt-get update
RUN DEBIAN_FRONTEND='noninteractive' apt-get install -qqy x11-apps python3 python3-pip python3-tk xvfb python-opengl ffmpeg x11-utils ghostscript
RUN pip3 install pyvirtualdisplay
ENV DISPLAY :0
# CMD xeyes
# FROM python:3.8
ADD requirements.txt /requirements.txt
# ADD main.py backend/main.py
ADD okteto-stack.yaml /okteto-stack.yaml
RUN pip3 install -r requirements.txt
EXPOSE 8080
COPY ./backend backend
CMD ["uvicorn", "backend.main:app", "--host=0.0.0.0", "--port=8080"]