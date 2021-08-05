from master import app
from user.view import api_route
from role.view import api_role
from master.view import api_view

app.register_blueprint(api_route)
app.register_blueprint(api_view)
app.register_blueprint(api_role)


if __name__ == "__main__":
    app.run(debug=True)
