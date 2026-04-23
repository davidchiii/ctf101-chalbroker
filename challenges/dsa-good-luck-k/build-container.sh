#!/bin/bash

openssl dsaparam -genkey 2048 >> ctf.key
docker build -t csaw .
