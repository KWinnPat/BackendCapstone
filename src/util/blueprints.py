import routes


def register_blueprint(app):
    app.register_blueprint(routes.auth)
    app.register_blueprint(routes.user)
    app.register_blueprint(routes.reservation)
    app.register_blueprint(routes.wishlist)
    app.register_blueprint(routes.wishlist_item)
    app.register_blueprint(routes.item)
    app.register_blueprint(routes.category)
    app.register_blueprint(routes.event)