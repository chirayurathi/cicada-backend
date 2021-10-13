from rest_framework.views import exception_handler

def customException(exc, context):

    response = exception_handler(exc, context)
    if response is not None:
        if response.data.get('detail'):
            response.data['message'] = response.data['detail']
            del response.data['detail']
        else:
            response.data['message'] = response.data
        response.data['success'] = False
    return response