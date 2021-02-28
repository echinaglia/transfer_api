import requests

host = 'http://account:80/api/Account/'


def get_account(account_number, origin=True):
    try:
        req = requests.get(host + account_number)
    except ConnectionError:
        return {}, 'Server is unstable, please try again later'

    if req.status_code == 200:
        return req.json(), ''
    elif req.status_code == 404:
        err = 'accountOrigin does not exist' if origin else 'accountDestination does not exist'
        return {}, err
    return {}, req.content


def post_transfer(transfer):
    try:
        debit = requests.post(host, json={"accountNumber": transfer['accountOrigin'], "value": transfer['value'],
                                          "type": "Debit"})
    except ConnectionError:
        return {}, 'Server is unstable, please try again later'

    if debit.status_code != 200:
        return debit.content

    try:
        credit = requests.post(host, json={"accountNumber": transfer['accountDestination'], "value": transfer['value'],
                                           "type": "Credit"})
    except ConnectionError:
        return {}, 'Server is unstable, please try again later'

    if credit.status_code != 200:
        try:
            rollback = requests.post(host, json={"accountNumber": transfer['accountOrigin'], "value": transfer['value'],
                                                 "type": "Credit"})
        except ConnectionError:
            return {}, 'Server is unstable, please try again later'

        if rollback.status_code != 200:
            return rollback.content
        return credit.content

    return ''
