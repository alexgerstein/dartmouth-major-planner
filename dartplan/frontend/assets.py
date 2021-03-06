import os
from flask.ext import assets

js_dartplan = assets.Bundle("dartplan.coffee",
                            "plans.coffee",
                            "users.coffee",
                            "terms.coffee",
                            "hours.coffee",
                            "medians.coffee",
                            "departments.coffee",
                            "distributives.coffee",
                            "courses.coffee",
                            "offerings.coffee",
                            "controllers.coffee",
                            "directives.coffee",
                            filters="coffeescript,rjsmin",
                            output="js/dartplan.js")

css_dartplan = assets.Bundle("dartplan.scss",
                             filters="pyscss,cssmin",
                             output="css/dartplan.css")


def init_app(app):
    webassets = assets.Environment(app)
    webassets.url = app.static_url_path

    # Tell flask-assets where to look for our coffeescript and scss files.
    webassets.load_path = [
        os.path.join(os.path.dirname(__file__), 'scss'),
        os.path.join(os.path.dirname(__file__), 'coffee'),
    ]

    webassets.register('js_dartplan', js_dartplan)
    webassets.register('css_dartplan', css_dartplan)
    webassets.manifest = 'cache' if not app.debug else False
    webassets.cache = not app.debug
    webassets.debug = app.debug
