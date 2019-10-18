# coding: utf8


class ApiError(Exception):
    def __init__(self, error):
        Exception.__init__(self)
        self.error = error

