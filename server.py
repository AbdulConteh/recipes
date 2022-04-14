from flask_app import app
from flask_app.controllers.recipes_controllers import Recipe 
from flask_app.controllers.users_controllers import User

if __name__=="__main__":
	app.run(debug=True)