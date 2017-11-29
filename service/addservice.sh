#!/bin/bash

SOLUTION_ID="$1"
BUSINESS_ID="$2"
EXCHANGE="$3"
if [[ -z "$SOLUTION_ID" ]]; then
    SOLUTION_ID="a27fp8y8qvukg0000"
fi
if [[ -z "$BUSINESS_ID" ]]; then
    BUSINESS_ID="6fd6oo3zryynwmi"
fi
if [[ -z "$EXCHANGE" ]]; then
    EXCHANGE="Y"
fi

SERVICE=("twilio" "auth0" "mbed" "bulknotify" "spms" "http" "salesforceiot" "postgresql" "scripts")
ELEMENTID=("5955b9efbf83ba00015fff45" "5955b9ecbf83ba00015fff3f" "59fc07e5a28459000146da6d" "59b6eb1ef50b8f0001dbfcc4" "5955b9edbf83ba00015fff43" "5a040251f0d1e8000102c3d5" "59facfb35e444400016a68f9")
Fail=0
count=0

if [[ "$EXCHANGE" == "Y" ]] || [[ "$EXCHANGE" == "N" ]] || [[ "$EXCHANGE" == "y" ]] || [[ "$EXCHANGE" == "n" ]]; then

    if [[ "$EXCHANGE" == "Y" ]] || [[ "$EXCHANGE" == "y" ]]; then
        printf "Purchase Start"
        for e in "${ELEMENTID[@]}"
        do
            printf "\n--------\n"
            printf "Purchase Element_ID: '$e' \n"
            printf "Purchase Element: ${SERVICE[count]} \n"
            RESP=$(curl -X POST 'https://bizapi-staging.hosted.exosite.io/api:1/exchange/'$BUSINESS_ID'/purchase/' \
            -H 'content-type: application/json' \
            -H 'Authorization: token 8865cdb1aec99a61241d874781b1f438d10a81d9' \
            -d '{"elementId":"'$e'"}' \
                -k --silent -L -w "\n%{http_code}" )

            STATUS="${RESP##*$'\n'}"           
            CONTENT="${RESP%$'\n'*}"

            if [[ "$STATUS" == 200 ]] ; then
                printf "200 Purchase Element Success ..... \n"
            elif [[ "$STATUS" == 409 ]] ; then
                printf "409 Purchase Element Fail : Conflict Purchase \n"
            elif [[ "$STATUS" == 403 ]] ; then
                printf "403 Purchase Element Fail : Permissions Decline , Please Upgrade Business \n"
                Fail=1
                break
            else
                printf "Not Expected Error : ${STATUS} ${CONTENT} \n"
                break
            fi
            printf "\n--------\n"
            count=$((++count))
        done
        printf "\n--------\n"
        printf "Purchase End\n"
    fi

    if [[ "$Fail" == 0 ]]; then
        printf "Service Adding Start\n"
        for i in "${SERVICE[@]}"
        do
            printf "\n--------\n"
            printf "Add Service: $i \n"
            RESP=$(
                curl 'http://localhost:8081/api/v1/solution/'$SOLUTION_ID'/serviceconfig' \
                     -H 'Content-Type: application/json' \
                     -X POST -d '{"service":"'$i'","solution_id":"'$SOLUTION_ID'"}' \
                     -k --silent -L -w "\n%{http_code}"
            )

            STATUS="${RESP##*$'\n'}"           
            CONTENT="${RESP%$'\n'*}"

            if [[ "$STATUS" == 200 ]] ; then
                printf "200 Add Service Success ..... \n"
            elif [[ "$STATUS" == 409 ]] ; then
                printf "409 Add Service Fail : Service Is Existing In Application \n"
            elif [[ "$STATUS" == 403 ]] ; then
                printf "403 Add Service Fail : Service Name InCorrect \n"
                break
            elif [[ "$STATUS" == 000 ]] ; then
                printf "Please login dqa-env/exo-openshift-hopper \n"
                break
            else
                printf "Not Expected Error : ${STATUS} ${CONTENT} \n"
                break
            fi
            printf "\n--------\n"
        done
        printf "\n--------\n"
        printf "Service Adding End\n"
    fi

else
    printf "\n--------\n"
    printf "Please input parameter : python addservice.sh <SOLUTION_ID> <BUSINESS_ID> <Purchase Y or N> \n"
    printf "\n--------\n"
fi

printf "\n -----------End----------\n"

