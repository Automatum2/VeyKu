from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from models.user import User
from models.respondent import Respondent
from models.survey_response import SurveyResponse
