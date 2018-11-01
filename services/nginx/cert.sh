#!/usr/bin/env bash

source ../../.env

rm cert/*.crt
rm cert/*.key

openssl req \
    -x509 \
    -out cert/$DOMAIN.crt \
    -keyout cert/$DOMAIN.key \
    -newkey rsa:2048 -nodes -sha256 \
    -subj "/CN=$DOMAIN" \
    -config "./cert/openssl.development.cnf" \
    -extensions v3_ca

# add to browser
certutil -d sql:$HOME/.pki/nssdb -A -t "P,," -n cert/$DOMAIN.crt -i cert/$DOMAIN.crt
certutil -d sql:$HOME/.pki/nssdb -L

for i in ./conf.d/*.conf; do
    sed -i -e "s/\/etc\/nginx\/cert\/enraged.local/\/etc\/nginx\/cert\/$DOMAIN/g" $i
done

