#!/usr/bin/env bash
ab -n 1000 -c 1000 -p data/data_format.json -T application/json -H "x-api-key: harvest" https://localhost:443/rpc/store
