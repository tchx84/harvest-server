#!/usr/bin/env bash
ab -n 10000 -c 1000 -p data/data.json -T application/json -H "x-api-key: harvest" https://localhost/rpc/store
