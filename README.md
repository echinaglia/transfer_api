# transfer_api

#running info

git clone git@github.com:echinaglia/transfer_api.git

cd transfer_api

docker-compose build

docker-compose up

# usage

get all accounts:
localhost:3000/api/Account/

post transfer
localhost:5000/api/fund-transfer

body = {"accountOrigin": "string", "accountDestination": "string", "value": decimal}

response = {"transactionId": "98ad80de-14cc-4e1f-9053-2ea2d8a7dc53"}

get tranfer status
localhost:5000/api/fund-transfer/{{transactionId}}

response = {"status": "string" // in_queue, processing, confirmed, error
            "message": "string"}
