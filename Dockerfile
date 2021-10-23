FROM continuumio/miniconda3
ADD environment.yml /tmp/environment.yml
RUN conda env create -f /tmp/environment.yml
RUN echo "source activate ocr" > ~/.bashrc
ENV PATH /opt/conda/envs/ocr/bin:$PATH
EXPOSE 5000
# Demonstrate the environment is activated:
RUN echo "Make sure flask is installed:"
RUN python -c "import flask"
RUN apt-get update \
    && apt-get install tesseract-ocr -y
# The code to run when container is started:
COPY iterate_pages.py .
COPY webapp/ ./webapp
RUN apt install -y vim
RUN cd webapp
CMD cd webapp && flask run --host=0.0.0.0
