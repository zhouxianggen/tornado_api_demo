# -*- coding: utf-8 -*-
import concurrent
from time import monotonic as now
from argparse import ArgumentParser
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.web import Application, RequestHandler
from tornado_api_demo.base import BaseError, get_logger, get_uuid
from tornado_api_demo.context import g_ctx


class ApiService(Application):
    def __init__(self):
        handlers = [
            (r"/(.+?)", ApiRequestHandler)
        ]
        settings = dict(
            debug=True,
        )
        Application.__init__(self, handlers, **settings)


class ApiRequestHandler(RequestHandler):
    executor = concurrent.futures.ThreadPoolExecutor(
            thread_name_prefix='worker')


    async def post(self, api):
        await self.on_request(api)


    async def get(self, api):
        await self.on_request(api)


    async def on_request(self, api):
        try:
            resp = await IOLoop.current().run_in_executor(
                    self.executor, self.process_request, api)
            self.finish({'status': 20000,  'data': resp})
        except Exception as e:
            self.finish({'status': 50000, 'error': str(e)})


    def process_request(self, api):
        # 构建请求上下文
        req = RequestContext(self.request, api)
        req.log.info('{} {} {}'.format(req.version, req.api, req.params))
        # 根据版本生成数据模型
        model = g_ctx.factory.gen(req.version)
        model.log = req.log
        impl = getattr(model, api, None)
        if not impl:
            raise BaseError('api not implemented')
        try:
            # 生成数据库session
            req.session = g_ctx.mksession(model.conn)
            r = impl(req)
            req.session.commit()
            return r
        except Exception as e:
            req.log.exception(e)
            req.session.rollback()
            raise
        finally:
            took = (now() - req.start_time) * 1000
            req.log.info('{} took {:.2f} ms'.format(api, took)) 
            req.session.close()


class RequestContext(object):
    def __init__(self, request, api):
        self.request = request
        self.api = api
        self.start_time = now()
        self.session_id = get_uuid()
        self.params = {k: v[0].decode('utf8') for k,v in 
            self.request.arguments.items() if v}
        self.version = self.params['version']
        self.log = get_logger(self.session_id)


def main():
    parser = ArgumentParser()
    parser.add_argument("-p", "--port", default=8888, type=int, 
            help="specify port")
    parser.add_argument("-c", "--config", required=True, 
            help="specify config file")
    args = parser.parse_args()
    g_ctx.init(args.config)
    service = HTTPServer(ApiService())
    service.listen(args.port)
    IOLoop.instance().start()


if __name__ == "__main__":
    main()

