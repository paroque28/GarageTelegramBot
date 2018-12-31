# base-image for python on any machine using a template variable,
# see more about dockerfile templates here:http://docs.resin.io/pages/deployment/docker-templates
FROM resin/intel-edison-python:3

# use apt-get if you need to install dependencies,
# for instance if you need ALSA sound utils, just uncomment the lines below.
# RUN apt-get update && apt-get install -yq \
#    alsa-utils libasound2-dev && \
#    apt-get clean && rm -rf /var/lib/apt/lists/*

# Build mraa
WORKDIR /mraa/build
RUN  cmake .. -DBUILDSWIGNODE=OFF
RUN make _python3-mraa
RUN cp src/python/python3/*mraa* /usr/local/lib/python3.6

#Clean up
WORKDIR /usr/src/app
RUN rm -rf /mraa

# Copy requirements.txt first for better cache on later pushes
COPY ./requirements.txt /requirements.txt

# pip install python deps from requirements.txt on the resin.io build server
RUN pip install -r /requirements.txt
RUN git clone https://github.com/python-telegram-bot/python-telegram-bot --recursive && cd python-telegram-bot && python setup.py install && cd .. && rm -rf python-telegram-bot
RUN echo ~
RUN dasdasda
# This will copy all files in our root to the working  directory in the container
COPY . ./

# switch on systemd init system in container
ENV INITSYSTEM on

# main.py will run when container starts up on the device
CMD ["python","-u","src/main.py"]
