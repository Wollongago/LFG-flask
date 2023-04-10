#!/bin/bash

getopt --test > /dev/null
if [[ $? -ne 4 ]]; then
    echo "I’m sorry, `getopt --test` failed in this environment."
    exit 1
fi

SHORT=q:n:b
LONG=queue,name,beat
GREEN='\033[01;32m'
PURPLE='\033[01;38;5;171m'
RED='\033[0;31m'
NO_COLOR="\033[00m"

BEAT="false"

# -temporarily store output to be able to check for errors
# -activate advanced mode getopt quoting e.g. via “--options”
# -pass arguments only via   -- "$@"   to separate them correctly
PARSED=`getopt --options $SHORT --longoptions $LONG --name "$0" -- "$@"`
if [[ $? -ne 0 ]]; then
    # e.g. $? == 1
    #  then getopt has complained about wrong arguments to stdout
    exit 2
fi
# use eval with "$PARSED" to properly handle the quoting
eval set -- "$PARSED"

# now enjoy the options in order and nicely split until we see --
while true; do
    case "$1" in
        -q|--queue)
            echo "$2"
            QUEUE="$2"
            shift 2
            ;;
        -n|--name)
            HOSTNAME="$2"
            shift 2
            ;;
        -b|--beat)
            BEAT="true"
            shift
            ;;
        --)
            shift
            break
            ;;
        *)
            echo "Programming error"
            exit 3
            ;;
    esac
done

LOGLEVEL="info"
DEVELOPMENT="${DEVELOPMENT:=False}"
echo "[CELERY] Dev mode: ${DEVELOPMENT}";
if [[ "$DEVELOPMENT" == "True" ]]; then
    LOGLEVEL='debug'
fi

echo "[CELERY] Loglevel: $LOGLEVEL"
echo "[CELERY] Queue: $QUEUE"
echo "[CELERY] Hostname: $HOSTNAME"

if [[ $BEAT == "true" ]]; then
	echo "[CELERY] Launch Celery Beat"
    rm -f /tmp/celerybeat.pid ; 
    exec celery \
        --workdir=/application \
        -A Celery.celery_tasks.celery_app \
        beat \
        --pidfile=/tmp/celerybeat.pid \
        -s /tmp/schedule.db \
        -l "$LOGLEVEL"
else
	echo "[CELERY] Launch Celery Worker"
    rm -f /tmp/celeryd.pid
    exec celery \
        --workdir=/application \
        -A Celery.celery_tasks.celery_app \
        worker \
        --pidfile=/tmp/celeryd.pid \
        -c 4 \
        -Q "$QUEUE" \
        -n "$HOSTNAME" \
        -E \
        -l "$LOGLEVEL"
fi
