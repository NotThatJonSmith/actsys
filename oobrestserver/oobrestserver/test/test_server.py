import os
import sys
import json

from cherrypy.test import helper

from ..Application import Application
from ..ParallelDispatcher import ParallelDispatcher


class TestServer(helper.CPWebCase):

    app = None

    @staticmethod
    def setup_server():

        app_path = os.path.dirname(os.path.realpath(__file__))
        if app_path not in sys.path:
            sys.path.append(app_path)

        config = {
            "node1": {
                "FooString": {
                    "#obj": ["DefaultProviders.StringDevice", "Foo"]
                },
                "HelloDevice": {
                    "#obj": ["DefaultProviders.HelloSensor"]
                },
                "folder": {
                    "InsideString": {
                        "#obj": ["DefaultProviders.StringDevice", "Inside"]
                    }
                },
                "exception_thrower": {
                    "#obj": ["DefaultProviders.ExceptionThrower"]
                }
            },
            "node2": {
                "FooString": {
                    "#obj": ["DefaultProviders.StringDevice", "Foo"]
                },
                "HelloDevice": {
                    "#obj": ["DefaultProviders.HelloSensor"]
                },
                "folder": {
                    "InsideString": {
                        "#obj": ["DefaultProviders.StringDevice", "Inside"]
                    }
                },
                "exception_thrower": {
                    "#obj": ["DefaultProviders.ExceptionThrower"]
                },
                "non_string_obj": {
                    "#obj": [17]
                }
            },
            "bad_noclass": {
                '#obj': ['']
            },
            "good_short": {
                "#obj": ['DefaultProviders.HelloSensor']
            },
            "bad_ctor": {
                "#obj": ["DefaultProviders.StringDevice", 'too', 'many', 'args']
            }
        }

        TestServer.app = Application(config)
        TestServer.app.mount()

    def teardown_class(cls):
        TestServer.app.cleanup()
        super(TestServer, cls).teardown_class()

    def test_json_urls(self):
        for url in [
                '/api/',
                '/api/node1/',
                '/api/node1/folder/',
                '/api/node1/folder/InsideString/',
                '/api/node1/folder/InsideString/string/',
                '/gui/',
                '/gui/node1/',
                '/gui/node1/folder/',
                '/gui/node1/folder/InsideString/',
                '/gui/node1/folder/InsideString/string/']:
            print('getting'+url)
            self.getPage(url)
            self.assertStatus('200 OK')

    def test_response_fields(self):
        self.getPage('/api/node1/folder/InsideString/string/')
        full_response = json.loads(self.body)
        response = full_response['node1/folder/InsideString/string']
        self.assertIn('exceptions', response)
        self.assertIn('samples', response)

    def test_simple_post(self):
        json_post = json.dumps('Barbar!')
        json_length = str(len(json_post))
        headers = [('Content-Type', 'application/json'),
                   ('Content-Length', json_length)]
        self.getPage('/api/node1/folder/InsideString/string', headers,
                     'POST', json_post)
        self.assertStatus('200 OK')
        self.check_exception_free_body()
        self.check_in_all_samples('/api/node1/folder/InsideString/string', 'Barbar!')

    def test_search_globstar(self):
        self.getPage('/api/node1**/string')
        self.assertStatus('200 OK')
        responses = json.loads(self.body)
        self.assertIn('node1/FooString/string', responses)
        self.assertIn('node1/folder/InsideString/string', responses)
        self.assertEqual(len(responses), 2)

    def test_search_star(self):
        self.getPage('/api/node1/*/string')
        self.assertStatus('200 OK')
        responses = json.loads(self.body)
        self.assertIn('node1/FooString/string', responses)
        self.assertNotIn('node1/folder/InsideString/string', responses)
        self.assertEqual(len(responses), 1)

    def test_search_brackets(self):
        self.getPage('/api/node[12]/FooString/string')
        self.assertStatus('200 OK')
        responses = json.loads(self.body)
        self.assertIn('node1/FooString/string', responses)
        self.assertIn('node2/FooString/string', responses)
        self.assertEqual(len(responses), 2)

    def test_search_negate_brackets(self):
        self.getPage('/api/node[!2]/FooString/string')
        self.assertStatus('200 OK')
        responses = json.loads(self.body)
        self.assertIn('node1/FooString/string', responses)
        self.assertNotIn('node2/FooString/string', responses)
        self.assertEqual(len(responses), 1)

    def test_search_qmark(self):
        self.getPage('/api/node%3F/HelloDevice/hello')
        self.assertStatus('200 OK')
        responses = json.loads(self.body)
        self.assertIn('node1/HelloDevice/hello', responses)
        self.assertIn('node2/HelloDevice/hello', responses)
        self.assertEqual(len(responses), 2)

    def test_get_many_samples(self):
        self.getPage('/api/node1/folder/InsideString/string?sample_rate=100&duration=0.25')
        self.assertStatus('200 OK')
        samples = json.loads(self.body)['node1/folder/InsideString/string']['samples']
        self.assertGreater(len(samples), 10)

    def test_glob_only_url(self):
        self.getPage('/api/**')
        self.assertStatus('200 OK')
        self.check_exception_free_body()

    def check_exception_free_body(self):
        doc = json.loads(self.body)
        for url in [url for url in doc if 'children' not in doc[url]]:
            print(url)
            if "exception" not in url:
                self.assertEqual(0, len(doc[url]['exceptions']))

    def test_multi_post(self):
        json_post = json.dumps('TEST')
        headers = [('Content-Type', 'application/json'),
                   ('Content-Length', str(len(json_post)))]
        self.getPage('/api/(node1|node2)/FooString/string', headers=headers, method='POST', body=json_post)
        self.assertStatus('200 OK')
        self.check_exception_free_body()
        self.check_in_all_samples('/api/(node1|node2)/FooString/string', 'TEST')

    def test_single_post_list_syntax(self):
        json_post = json.dumps('TEST')
        headers = [('Content-Type', 'application/json'),
                   ('Content-Length', str(len(json_post)))]
        self.getPage('/api/(node1)/FooString/string', headers=headers, method='POST', body=json_post)
        self.assertStatus('200 OK')
        self.check_exception_free_body()
        self.check_in_all_samples('/api/(node1)/FooString/string', 'TEST')

    def check_in_all_samples(self, url, string):
        self.getPage(url)
        doc = json.loads(self.body)
        for record in doc:
            self.assertIn(string, doc[record]['samples'])

    def test_get_many_values_many_samples(self):
        self.getPage('/api/node1/**/string?sample_rate=100&duration=0.25')
        self.assertStatus('200 OK')
        responses = json.loads(self.body)
        self.assertEqual(len(responses), 2)
        for path in responses:
            self.assertGreater(len(responses[path]['samples']), 10)

    def test_exception_in_result(self):
        self.getPage('/api/node2/exception_thrower/exception')
        self.assertStatus('200 OK')
        exceptions = json.loads(self.body)['node2/exception_thrower/exception']['exceptions']
        self.assertIn('Example Exception', exceptions)
        self.getPage('/api/node2/exception_thrower/exception?sample_rate=10&duration=0.25')
        self.assertStatus('200 OK')
        exceptions = json.loads(self.body)['node2/exception_thrower/exception']['exceptions']
        self.assertIn('Example Exception', exceptions)
        self.assertGreater(len(exceptions), 1)

    def test_bad_configs(self):

        self.getPage('/api/good_short/hello')
        self.assertStatus('200 OK')
        self.assertIn('Hello World!', self.body)

        self.getPage('/api/bad_ctor/*')
        self.assertStatus("200 OK")
        self.assertBody('{}')

        self.getPage('/api/bad_noclass')
        self.assertStatus("200 OK")
        self.assertBody('{"bad_noclass": {"children": {}}}')

        self.getPage('/api/17')
        self.assertStatus("404 Not Found")

        self.getPage('/api/foobar')
        self.assertStatus("404 Not Found")

    def test_bad_glob(self):
        self.getPage('/api/100[1-4')
        self.assertStatus("400 Bad Request")
