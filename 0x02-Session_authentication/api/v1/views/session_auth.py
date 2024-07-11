#!/usr/bin/env python3
"""Module of SessionAuth views"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def view_session_auth() -> str:
    """ POST /api/v1/auth_session/login """
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({'error': 'email missing'}), 400
    if not password:
        return jsonify({'error': 'password missing'}), 400
    try:
        from models.user import User
        users = User.search({'email': email})
    except Exception:
        return jsonify({'error': 'no user found for this email'}), 404
    if not users:
        return jsonify({'error': 'no user found for this email'}), 404
    valid_user = None
    for user in users:
        if user.is_valid_password(password):
            valid_user = user
            break
    if not valid_user:
        return jsonify({'error': 'wrong password'}), 401
    from api.v1.app import auth
    session_id = auth.create_session(valid_user.id)
    response = jsonify(valid_user.to_json())
    response.set_cookie(getenv('SESSION_NAME'), session_id)
    return response
