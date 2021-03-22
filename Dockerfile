FROM python:3.9-slim-buster as build
WORKDIR /build
COPY src/ ./src/
COPY setup.py ./
RUN python setup.py bdist_wheel

FROM python:3.9-slim-buster
RUN groupadd -r friss \
    && useradd -r -u 1000 -g friss -s /bin/bash friss
RUN mkdir /opt/friss-matcher /opt/friss-matcher/data \
    && chown friss:friss /opt/friss-matcher -R
USER friss
ENV HOME /opt/friss-matcher
ENV PATH "/opt/friss-matcher/.local/bin:${PATH}"
ENV BASE_DIR "/opt/friss-matcher/data"
WORKDIR /opt/friss-matcher
COPY --from=build /build/dist/friss_matcher-*.whl /opt/friss-matcher/
RUN pip install /opt/friss-matcher/friss_matcher-*.whl --user
