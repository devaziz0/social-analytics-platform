FROM python:3

ENV APP_DIR_NAME SocialAnalyticsProject
ENV APP_PATH /opt/$APP_DIR_NAME


#installing django
COPY requirements.txt /
RUN pip3 install -r requirements.txt
RUN rm requirements.txt
RUN pip3 install sklearn
RUN pip3 install Flask

#adding the django project
RUN mkdir -p $APP_PATH
COPY $APP_DIR_NAME $APP_PATH

# create celery user
RUN useradd -N -M --system -s /bin/bash celery && echo celery:"B1llyB0n3s" | /usr/sbin/chpasswd
# celery perms
RUN groupadd grp_celery && usermod -a -G grp_celery celery && mkdir -p /var/run/celery/ /var/log/celery/
RUN chown -R celery:grp_celery /var/run/celery/ /var/log/celery/
# copy celery daemon files
ADD /config/celery/celeryd /etc/init.d/celeryd
RUN chmod +x /etc/init.d/celeryd
ADD /config/celery/celerybeat /etc/init.d/celerybeat
RUN chmod 750 /etc/init.d/celeryd /etc/init.d/celerybeat
RUN chown root:root  /etc/init.d/celeryd /etc/init.d/celerybeat
# copy celery config
ADD /config/celery/celerydefault /etc/default/celeryd
ADD /config/celery/beatdefault /etc/default/celerybeat

RUN chmod 640 /etc/default/celeryd
RUN chmod 640 /etc/default/celerybeat

RUN groupadd --system supervisord && useradd --system --gid supervisord supervisord

RUN chmod 1777 /tmp

RUN apt-get update \
    && apt-get install -y supervisor \
    && mkdir -p /var/log/supervisord/ \
    && chown -R supervisord:supervisord /var/log/supervisord

ADD /config/celery/supervisord-worker.conf /supervisord-worker.conf
ADD /config/celery/supervisord-beat.conf /supervisord-beat.conf
