# importing libraries
from flask import Flask, request, Response, jsonify
from flasgger import Swagger
import logging
from logging.handlers import SMTPHandler
from flask_sqlalchemy import SQLAlchemy


# creating an instance of the flask app
app = Flask(__name__)
logging.basicConfig(filename='VOIXCA_API.log', level=logging.WARNING, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
swagger = Swagger(app)

# Configure our Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Configure log mail
mail_handler = SMTPHandler (
    mailhost = ('smtp.gmail.com', 587),
    fromaddr = 'manondbt.servererror@gmail.com',
    toaddrs = ['manondebout41@gmail.com'],
    subject = 'Application Error',
    credentials = ('manondbt.servererror@gmail.com','P@ssword1234'),
    secure = ()
)
mail_handler.setLevel(logging.CRITICAL)
mail_handler.setFormatter(logging.Formatter(
    '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
))
app.logger.addHandler(mail_handler)
