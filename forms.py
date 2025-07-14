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
    header = StringField("Header", validators=[DataRequired()])
    paragraph1 = TextAreaField("Paragraph 1", validators=[DataRequired()])
    paragraph2 = TextAreaField("Paragraph 2", validators=[DataRequired()])
    subtext1 = StringField("Subtext 1", validators=[DataRequired()])
    subtext2 = StringField("Subtext 2", validators=[DataRequired()])
    footer = StringField("Footer", validators=[DataRequired()])

    # Color pickers
    header_color = StringField("Header/Footer Color", default="#ffffff")
    para1_color = StringField("Paragraph 1 Color", default = "#0070C0")
    para2_color = StringField("Paragraph 2 Color", default= "black")
    subtext_color = StringField("Subtext Color", default="#ffffff")

    # Font sizes
    header_size = StringField("Header/Footer Font Size (px)", default="11")
    paragraph_size = StringField("Paragraph Font Size (px)", default="46")
    subtext_size = StringField("Subtext Font Size (px)", default="18")

    submit = SubmitField("Generate Advertisement")