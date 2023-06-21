#/bin/bash

getopt --test > /dev/null
if [[ $? -ne 4 ]]; then
    echo "I’m sorry, `getopt --test` failed in this environment."
    exit 1
fi

SHORT=c:f:m:
LONG=case:,file:,method:
GREEN='\033[01;32m'
PURPLE='\033[01;38;5;171m'
RED='\033[0;31m'
NO_COLOR="\033[00m"

CASE=''

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
        -c|--case)
            CASE="$2"
            shift 2
            ;;
        -f|--file)
            FILENlfgE="$2"
            shift 2
            ;;
        -m|--method)
            CLASSS_METHOD="$2"
            shift 2
            ;;
        --)
            shift
            break
            ;;
        *)
            echo "Progrlfgming error"
            exit 3
            ;;
    esac
done

echo -e ""
echo -e "${GREEN}Run tests${NO_COLOR}"
echo -e ""


if [ -n "${FILENlfgE:+x}" ] && [ ! -z ${CASE} ];then
    # echo;
    echo -e "${GREEN}Case: ${PURPLE}${CASE}${NO_COLOR}"
    echo -e "${GREEN}File: ${PURPLE}${FILENlfgE}${NO_COLOR}"
    if [ ! -z ${CLASSS_METHOD} ]; then
        echo -e "${GREEN}Class and method: ${PURPLE}${CLASSS_METHOD}${NO_COLOR}"
        docker-compose -p lfg exec lfg-flask /bin/bash -c "python3 -W ignore:ResourceWarning -m unittest -v Tests.cases.${CASE}.${FILENlfgE}.${CLASSS_METHOD}"
    else
        docker-compose -p lfg exec lfg-flask /bin/bash -c "python3 -W ignore:ResourceWarning -m unittest -v Tests.cases.${CASE}.${FILENlfgE}"
    fi
elif [ ! -z ${CASE} ]; then
    echo -e "${GREEN}Case: ${PURPLE}${CASE}${NO_COLOR}"
    docker-compose -p lfg exec lfg-flask /bin/bash -c "python3 -W ignore:ResourceWarning -m unittest discover -v -s Tests/cases/${CASE}"
else
    docker-compose -p lfg exec lfg-flask /bin/bash -c "python3 -W ignore:ResourceWarning -m unittest discover -v -s Tests/cases"
fi
