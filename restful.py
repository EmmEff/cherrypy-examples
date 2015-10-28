#!/usr/bin/env python

"""
Simple CherryPy example using Routes dispatcher and JSON output.  Suitable
for use as a starting framework for RESTful webservice API, for example

This script requires the following Python modules:

    * CherryPy (developed on 3.8.0)
    * Routes (developed on 2.2)

"""

import cherrypy
import json


__AUTHOR__ = 'Mike Frisch <mikef17@gmail.com>'


class JSONHTTPError(cherrypy.HTTPError):
    """
    Custom CherryPy HTTPError allowing setting status and error message
    and formatting it as JSON
    """

    def __init__(self, status=400, message=None):
        super(self.__class__, self).__init__()

        self.__status = status
        self.__message = message

    def set_response(self):
        """Override the default method"""

        cherrypy.response.headers['Content-Type'] = 'application/json'
        cherrypy.response.status = self.__status
        cherrypy.response.body = json.dumps({
            'error': self.__message if self.__message else '(none)',
        })


class ItemsController(object):
    """Controller for /nodes URL"""

    @cherrypy.tools.json_out()
    def get_items(self, name=None):
        """
        Handle /items and /items/:(name) GET requests
        """

        if name is None:
            return [
                'item1',
                'item2',
            ]

        if name not in ('item1', 'item2',):
            raise JSONHTTPError(404, message='Item [%s] not found' % (name))

        return {'item': {'name': name}}


def main():
    items_controller = ItemsController()

    dispatcher = cherrypy.dispatch.RoutesDispatcher(explicit=False)

    dispatcher.connect('get_items', '/items', action='get_items',
                       controller=items_controller,
                       conditions={'method': ['GET']})

    dispatcher.connect('get_items', '/items/:(name)', action='get_items',
                       controller=items_controller,
                       conditions={'method': ['GET']})

    config = {
        '/': {
            'request.dispatch': dispatcher,
        }
    }

    cherrypy.tree.mount(root=None, config=config)

    # Listen on port 5000
    cherrypy.config.update({'server.socket_port': 5000})

    cherrypy.engine.start()
    cherrypy.engine.block()


if __name__ == '__main__':
    main()
