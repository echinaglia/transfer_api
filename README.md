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
url: localhost:5000/api/fund-transfer

body:
'''json
{
  "accountOrigin": "string",
  "accountDestination": "string",
  "value": decimal
}
'''

response:
'''json
{
  "transactionId": "98ad80de-14cc-4e1f-9053-2ea2d8a7dc53"
}
'''

get tranfer status
url: localhost:5000/api/fund-transfer/{{transactionId}}

response:
'''json
{
  "status": "string" // in_queue, processing, confirmed, error
  "message": "string"
}
