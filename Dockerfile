FROM openfabric/tee-python-gpu:experimental
RUN mkdir application
WORKDIR /application
COPY . .
# This will download the model
#RUN poetry run python chat.py
RUN poetry install -vvv --no-dev
#RUN poetry run python chat.py
EXPOSE 5500
CMD ["sh","start.sh"]