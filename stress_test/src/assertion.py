def check_http_response(transaction, response):
    response_body = response.json()

    if transaction == 'send_question':
        if response_body['answer'] != 'рейтинг фильма гладиатор составляет 8.5':
            response.failure(response_body)
