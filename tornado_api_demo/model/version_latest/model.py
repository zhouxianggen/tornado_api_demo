# coding: utf8 
from tornado_api_demo.context import g_ctx
from tornado_api_demo.base import BaseObject, BaseError, get_uuid, use_cache
from tornado_api_demo.model.version_latest.entity import User, jsonify 


class Model(BaseObject):
    conn = 'test'

    @use_cache(g_ctx.cache, 'user', ['user_id'], ex=5)
    def _get_user(self, req):
        user_id = req.params['user_id']
        user = req.session.query(User).filter(User.uuid==user_id).first()
        if not user:
            raise BaseError('用户不存在')
        return {'user': jsonify(user)}


    def _add_user(self, req):
        user = User()
        user.uuid = get_uuid()
        user.nickname = req.params['nickname']
        req.session.add(user)
        return {'user': jsonify(user)}

