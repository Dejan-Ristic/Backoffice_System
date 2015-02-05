from flask import render_template, request, jsonify
from . import allusers


@allusers.app_errorhandler(404)
def page_not_found(e):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'not found'})
        response.status_code = 404
        return response
    return render_template('error/404.html'), 404


@allusers.app_errorhandler(500)
def page_not_found(e):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'internal server error'})
        response.status_code = 500
        return response
    return render_template('error/500.html'), 500


@allusers.app_errorhandler(403)
def page_not_found(e):
    return render_template('error/403.html'), 403