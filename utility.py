from flask import jsonify


def standard_response(data=None, code=200, status="success"):
    response = {
        "code": code,
        "status": status
    }
    if data is not None:
        response['data'] = data
    return jsonify(response), code