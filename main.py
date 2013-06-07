#!/usr/bin/env python
##
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

__author__  = 'Flavio C. Coelho (@fccoelho)'
__website__ = 'fccoelho.github.com'

import os, sys
# Third party libraries path must be fixed before importing webapp2
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'justice/external'))

import webapp2

import routes
from justice import routes as justice_routes
from admin import routes as admin_routes
from justice import config as justice_config
import config
from justice.lib.basehandler import handle_error

webapp2_config = justice_config.config
webapp2_config.update(config.config)

app = webapp2.WSGIApplication(debug = os.environ['SERVER_SOFTWARE'].startswith('Dev'), config=webapp2_config)

for status_int in app.config['error_templates']:
    app.error_handlers[status_int] = handle_error

routes.add_routes(app)
justice_routes.add_routes(app)
admin_routes.add_routes(app)


