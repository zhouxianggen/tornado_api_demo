# coding: utf8 
from tornado_api_demo.context import g_ctx
from tornado_api_demo.errors import ApiError
from tornado_api_demo.util import get_uuid, use_cache, del_cache
from tornado_api_demo.model.v100.entity import User, jsonify 


class Model(object):
    conn = 'test'

    @use_cache(g_ctx.cache, 'user', ['user_id'], ex=5)
    def _get_user(self, req):
        user_id = req.params['user_id']
        user = req.session.query(User).filter(User.uuid==user_id).first()
        if not user:
            raise ApiError('用户不存在')
        return {'user': jsonify(user)}


    def _add_user(self, req):
        user = User()
        user.uuid = get_uuid()
        user.nickname = req.params['nickname']
        req.session.add(user)
        return {'user': jsonify(user)}


    @del_cache(g_ctx.cache, 'user', ['user_id'])
    def _update_user(self, req):
        user_id = req.params['user_id']
        user = req.session.query(User).filter(User.uuid==user_id).first()
        if not user:
            raise ApiError('用户不存在')
        user.nickname = req.params['nickname']
        return {'user': jsonify(user)}

