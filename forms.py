from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    phone = StringField("Phone", validators=[DataRequired()])
    claim = TextAreaField("Claim", validators=[DataRequired()])
    submit = SubmitField("Submit")

class LandingPageForm(FlaskForm):
    custom_path = StringField("Page URL", validators=[DataRequired()])
    heading1 = StringField("Heading 1", validators=[DataRequired()])
    paragraph1 = TextAreaField("Paragraph 1", validators=[DataRequired()])
    heading2 = StringField("Heading 2", validators=[DataRequired()])
    paragraph2 = TextAreaField("Paragraph 2", validators=[DataRequired()])
    submit = SubmitField("Generate Landing Page")

class AdForm(FlaskForm):
    paragraph1 = TextAreaField("Paragraph 1", validators=[DataRequired()])
    paragraph2 = TextAreaField("Paragraph 2", validators=[DataRequired()])
    company_name = StringField("Company Name", validators=[DataRequired()])
    submit = SubmitField("Generate Advertisement")
