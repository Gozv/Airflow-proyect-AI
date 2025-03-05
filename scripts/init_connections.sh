#!/bin/bash

airflow connections add 'postgres_default' \
    --conn-type 'postgres' \
    --conn-host 'postgres' \
    --conn-login ${POSTGRES_USER} \
    --conn-password ${POSTGRES_PASSWORD} \
    --conn-schema ${POSTGRES_DB}

airflow connections add 'aws_default' \
    --conn-type 'aws' \
    --conn-extra "{\"aws_access_key_id\": \"${AWS_ACCESS_KEY_ID}\", \"aws_secret_access_key\": \"${AWS_SECRET_ACCESS_KEY}\", \"region_name\": \"${AWS_REGION}\"}"