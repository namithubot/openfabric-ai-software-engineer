FROM openfabric/tee-python-gpu:experimental
RUN mkdir application
WORKDIR /application
COPY . .
RUN poetry install --no-root
# This will download the model
RUN poetry run python chat.py
RUN poetry install -vvv --no-dev
EXPOSE 5500
CMD ["sh","start.sh"]