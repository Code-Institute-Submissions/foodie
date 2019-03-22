from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError


class SignForm(FlaskForm):

    # Fields - require some validation
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Submit')

    # username
    def validate_username(self, username):
        if len(username.data) < 4:
            raise ValidationError('username must be longer than 4 characters')

    # password
    def validate_password(self, password):
        if len(password.data) < 4:
            raise ValidationError('password must be longer than 4 characters')


# Editor Form
def EditorForm(*args, data):

    # Placeholder Class
    class StaticForm(FlaskForm):
        title = StringField('title', validators=[DataRequired()])
        author = StringField('author', validators=[DataRequired()])

    if args[0]:
        StaticForm.title = StringField('title', validators=[DataRequired()], default=data['details']['title'])
        StaticForm.author = StringField('author', validators=[DataRequired()], default=data['details']['author'])

    return StaticForm()


