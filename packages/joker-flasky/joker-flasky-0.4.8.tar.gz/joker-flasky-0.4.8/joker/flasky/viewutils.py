#!/usr/bin/env python3
# coding: utf-8

import datetime
import decimal
import functools
import mimetypes
import re
from typing import Union

import flask
import flask.views
from volkanic.utils import merge_dicts


def infer_mimetype(filename: str, default="text/plain") -> str:
    if '.' not in filename:
        filename = '_.' + filename
    elif filename.startswith('.'):
        filename = '_' + filename
    return mimetypes.guess_type(filename)[0] or default


infer_mime_type = infer_mimetype


def respond(*args, **kwargs):
    resp = kwargs
    for arg in args:
        if 'message' not in resp and isinstance(arg, str):
            resp['message'] = arg
            continue
        if 'data' not in resp:
            if isinstance(arg, (dict, int, float, str)):
                resp['data'] = arg
                continue
            if isinstance(arg, (list, tuple, set, frozenset)):
                resp['data'] = list(arg)
                continue
        r = repr(arg)
        msg = f'redundant or invalid argument for respond(): {r}'
        raise TypeError(msg)
    if resp.setdefault('code', 0):
        msg = 'for non-zero code, raise DomainError/TechnicalError instead.'
        raise TypeError(msg)
    return resp


def respond_content(
        content: Union[bytes, str],
        mimetype: str = None,
        headers: dict = None):
    resp = flask.make_response(content, 200)
    if headers:
        for key, val in headers.items():
            resp.headers.set(key, val)
    if mimetype:
        resp.mimetype = mimetype
    elif isinstance(content, str):
        resp.mimetype = "text/plain"
    else:
        resp.mimetype = 'application/octet-stream'
    return resp


def respond_plain_text(text: str, headers: dict = None):
    return respond_content(text, "text/plain", headers)


def respond_with_pre_gzipped(
        content: bytes, content_type=None, headers: dict = None):
    content_type = content_type or 'text/plain'
    headers = headers or {}
    headers['Content-Encoding'] = 'gzip'
    return respond_content(content, content_type, headers)


def respond_binary(content: bytes, content_type: str, headers: dict = None):
    return respond_content(content, content_type, headers)


def respond_xaccel_redirect(path: str, filename: str = None):
    # nginx: http://wiki.nginx.org/NginxXSendfile
    resp = flask.make_response()
    headers = {
        'X-Accel-Redirect': path,
        'Cache-Control': 'no-cache',
        'Content-Type': infer_mime_type(path, 'application/octet-stream'),
        'Content-Disposition':
            f'attachment; filename={filename}' if filename else 'inline',
    }
    resp.headers.update(headers)
    return resp


def get_request_data(force_json=False):
    request = flask.request
    if request.method == 'GET':
        return request.args.to_dict()
    if force_json or request.is_json:
        data = request.get_json(force=force_json)
        if not isinstance(data, dict):
            data = {'': data}
    else:
        data = request.form.to_dict()
    return merge_dicts(data, request.args)


class _ReducedViewMixin:
    force_json = False

    def get_request_data(self):
        return get_request_data(self.force_json)


class ReducedView(flask.views.View, _ReducedViewMixin):
    def dispatch_request(self):
        return self.__call__()

    def __call__(self):
        return respond()


class ReducedRestfulView(flask.views.MethodView, _ReducedViewMixin):
    pass


def jsonp(data, callback):
    return flask.current_app.response_class(
        callback + '(' + flask.json.dumps(data) + ');\n',
        mimetype='application/javascript'
    )


def fmt_datetime(o: datetime.datetime):
    if isinstance(o, datetime.datetime):
        return o.strftime('%Y-%m-%d %H:%M:%S')
    raise TypeError


def json_default_strict(o):
    if isinstance(o, decimal.Decimal):
        return float(o)
    if isinstance(o, datetime.timedelta):
        return o.total_seconds()
    if isinstance(o, datetime.datetime):
        return o.strftime('%Y-%m-%d %H:%M:%S')
    if isinstance(o, datetime.date):
        return o.isoformat()
    if hasattr(o, 'as_json_serializable'):
        return o.as_json_serializable()
    raise TypeError


def call_json_default_functions(o, funcs: Union[tuple, list] = None):
    funcs = funcs or []
    for func in funcs:
        try:
            return func(o)
        except TypeError:
            continue
    raise TypeError


def json_default(o):
    """usage: json.dumps(some_o, default=json_default)"""
    funcs = [json_default_strict, str]
    return call_json_default_functions(o, funcs)


def chain_json_default_functions(*funcs):
    return functools.partial(call_json_default_functions, funcs=funcs)


class JSONEncoderPlus(flask.json.JSONEncoder):
    json_default_funcs = [json_default_strict, str]

    def default(self, o):
        try:
            return call_json_default_functions(o, self.json_default_funcs)
        except TypeError:
            return super().default(o)


def get_json_encoder(*json_default_funcs):
    # bases should be a tuple
    bases = JSONEncoderPlus,
    attrs = {'json_default_funcs': list(json_default_funcs)}
    return type('JSONEncoderExtended', bases, attrs)


def serialize_current_session(app: flask.Flask = None):
    if app is None:
        app = flask.current_app
    ss = app.session_interface.get_signing_serializer(app)
    return ss.dumps(dict(flask.session))


class RequestBoundSingletonMeta(type):
    def __call__(cls, *args, **kwargs):
        cache = flask.g.setdefault('request_bound_cache', {})
        try:
            return cache[cls]
        except KeyError:
            obj = super().__call__(*args, **kwargs)
            return cache.setdefault(cls, obj)


def is_mobile():
    _regex_ua_mobile = re.compile(
        "Mobile|iP(hone|od|ad)|Android|BlackBerry|IEMobile|Kindle"
        "|NetFront|Silk-Accelerated|(hpw|web)OS|Fennec|Minimo"
        "|Opera M(obi|ini)|Blazer|Dolfin|Dolphin|Skyfire|Zune"
    )
    ua = flask.request.headers.get('User-Agent', '')
    return _regex_ua_mobile.search(ua)


def is_wechat():
    return 'micromessenger' in flask.request.user_agent.string.lower()


def decorate_all_view_funcs(app, decorator):
    keys = list(app.view_functions)
    for key in keys:
        func = app.view_functions[key]
        app.view_functions[key] = decorator(func)


def url_for_this(**values):
    # https://github.com/pallets/flask/issues/2111
    return flask.url_for(flask.request.endpoint, **values)
