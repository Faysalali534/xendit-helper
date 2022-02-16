import base64
import http.client
import json


def get_conn_headers():
    token = base64.b64encode(
        b"<token>:").decode("ascii")
    conn = http.client.HTTPSConnection("api.xendit.co")
    headers = {
        'Content-Type': "application/json",
        'Authorization': 'Basic %s' % token
    }
    return {
        "conn": conn,
        "headers": headers
    }


def get_balance():
    """
    :return: balance for the current account
    """
    conn_headers = get_conn_headers()
    conn = conn_headers['conn']
    headers = conn_headers['headers']
    conn.request("GET", "/balance", "", headers)
    return conn.getresponse().read().decode()


def create_account(email, account_type="MANAGED", public_profile=None):
    """
    :param email:
    :param account_type:
    :param public_profile:
    :return: created account
    """
    conn_headers = get_conn_headers()
    conn = conn_headers['conn']
    headers = conn_headers['headers']
    if account_type == "MANAGED":
        data = json.dumps({
            "email": email,
            "type": "MANAGED"
        })
    elif account_type == "OWNED":
        data = json.dumps({
            "email": email,
            "type": account_type,
            "public_profile": public_profile
        })
    else:
        return "Account type should be OWNED or MANAGED"
    conn.request("POST", "/v2/accounts", data, headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")


def transfer(reference, source_user, dest_user, amount):
    """
    :param reference:
    :param source_user:
    :param dest_user:
    :param amount:
    :return: transferred object
    """
    conn_headers = get_conn_headers()
    conn = conn_headers['conn']
    headers = conn_headers['headers']
    data = json.dumps({
        "reference": reference,
        "amount": amount,
        "source_user_id": source_user,
        "destination_user_id": dest_user
    })
    conn.request("POST", "/transfers", data, headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")


def create_customers(reference_id, email, name, for_user_id):
    """
    :param reference_id:
    :param email:
    :param name:
    :param for_user_id:
    :return: created customer
    """
    conn_headers = get_conn_headers()
    conn = conn_headers['conn']
    headers = conn_headers['headers']
    individual_detail = {
        "given_names": name,
    }
    data = json.dumps({
        "reference_id": reference_id,
        "email": email,
        "individual_detail": individual_detail
    })
    conn.request("POST", "/customers?for-user-id={}".format(for_user_id), data, headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")


def get_transactions():
    """
    :return: all transactions
    """
    conn_headers = get_conn_headers()
    conn = conn_headers['conn']
    headers = conn_headers['headers']
    conn.request("GET", "/transactions", "", headers)
    return conn.getresponse().read().decode()


def get_transaction_by_id(transaction_id):
    """
    :param transaction_id:
    :return: transaction object
    """
    conn_headers = get_conn_headers()
    conn = conn_headers['conn']
    headers = conn_headers['headers']
    conn.request("GET", "/transactions/{}".format(transaction_id), "", headers)
    return conn.getresponse().read().decode()


def create_virtual_account(external_id, bank_code, name, virtual_account_number, for_user_id=None, with_fee_rule=None):
    """
    :param external_id:
    :param bank_code:
    :param name:
    :param virtual_account_number:
    :param for_user_id:
    :param with_fee_rule:
    :return: virtual bank account for a customer
    """
    conn_headers = get_conn_headers()
    conn = conn_headers['conn']
    headers = conn_headers['headers']
    data = json.dumps({
        "external_id": external_id,
        "bank_code": bank_code,
        "name": name,
        "virtual_account_number": virtual_account_number,
    })
    conn.request("POST", "/callback_virtual_accounts?for-user-id={}".format(for_user_id), data, headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")


def get_virtual_account(account_id):
    """
    :param account_id:
    :return: virtual bank account of a customer
    """
    conn_headers = get_conn_headers()
    conn = conn_headers['conn']
    headers = conn_headers['headers']
    conn.request("GET", "/callback_virtual_accounts/{}".format(account_id), "", headers)
    return conn.getresponse().read().decode()


def get_all_virtual_accounts():
    """
    :return: all virtual bank accounts of customers
    """
    conn_headers = get_conn_headers()
    conn = conn_headers['conn']
    headers = conn_headers['headers']
    conn.request("GET", "/available_virtual_account_banks", "", headers)
    return conn.getresponse().read().decode()


def update_virtual_account(account_id, external_id=None):
    """
    :param account_id:
    :param external_id:
    :return: updated virtual bank account of a customer
    """
    conn_headers = get_conn_headers()
    conn = conn_headers['conn']
    headers = conn_headers['headers']
    data = json.dumps({
        "external_id": external_id,
    })
    conn.request("PATCH", "/callback_virtual_accounts/{}".format(account_id), data, headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")


def customer_payment_process(external_id, amount):
    """
    :param external_id:
    :param amount:
    :return: payment for a customer
    """
    conn_headers = get_conn_headers()
    conn = conn_headers['conn']
    headers = conn_headers['headers']
    data = json.dumps({
        "amount": amount,
    })
    conn.request("POST", "/callback_virtual_accounts/external_id={}/simulate_payment".format(external_id), data,
                 headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")


def create_fee_rule(amount):
    """
    :param amount:
    :return: created fee rule
    """
    conn_headers = get_conn_headers()
    conn = conn_headers['conn']
    headers = conn_headers['headers']
    data = json.dumps({
        "name": "standard_platform_fee",
        "description": "fee_for_all_transactions_accepted_on_behalf_of_vendors",
        "routes": [{
          "unit": "flat",
          "amount": amount,
          "currency": "IDR"
        }]
    })
    conn.request("POST", "/fee_rules", data, headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")


def create_invoice(external_id, amount, payer_email, description):
    """
    :param external_id:
    :param amount:
    :param payer_email:
    :param description:
    :return: created invoice
    """
    conn_headers = get_conn_headers()
    conn = conn_headers['conn']
    headers = conn_headers['headers']
    data = json.dumps({
        "external_id": external_id,
        "amount": amount,
        "payer_email": payer_email,
        "description": description
    })
    conn.request("POST", "/v2/invoices", data, headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")


if __name__ == '__main__':
    # print(get_balance())
    # print(create_account("faisal7@r4m.work"))
    # print(transfer("Testing transfer21", "620cea1456b580129250763c", "620cea3af9ea02829793d6a7", 1000))
    # print(create_customers("test_343", "faisal5@r4m.work", "Faisal", "6207600af06623911d380103"))
    # print(get_transactions())
    print(create_virtual_account("1", "BCA", "Faisal", "9999100141"))
    # print(get_virtual_account("620bc6b3382afc4797a4a04a"))
    # print(update_virtual_account("620bc6b3382afc4797a4a04a", "123"))
    # print(get_all_virtual_accounts())
    # print(customer_payment_process("123", 1000))
    # print(create_fee_rule(100))
    # print(create_invoice("test", 100, "faisal5@r4m.work", "demo invoice"))

    # faisal6@r4m.work 620cea1456b580129250763c
    # faisal7@r4m.work 620cea3af9ea02829793d6a7