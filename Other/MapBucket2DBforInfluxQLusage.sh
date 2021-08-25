curl --request POST http://192.168.1.193:8086/api/v2/dbrps \
  --header "Authorization: Token 8i8q6x5GdOlOtoaGa4o6nKENBJVpvI0z9y05yUfyYt5ln6TN9Gb8tdaHJkoZHupt6b8uVx9vCJOnzCZxv-OGZA==" \
  --header 'Content-type: application/json' \
  --data '{
        "bucketID": "266525e0f50b37fb",
        "database": "logger-bucket",
        "default": true,
        "orgID": "e675aff9e9e606c4",
        "retention_policy": "example-rp"
      }'
