from flask import Flask, render_template, redirect, session, send_file
from forms import ContactForm, LandingPageForm, AdForm
from utils import generate_ad_image, save_to_google_sheet  # moved from app.py
import os

app = Flask(__name__)
app.secret_key = "secret-key"

# In-memory store of generated pages
generated_pages = {}

@app.route("/", methods=["GET", "POST"])
def generate():
    form = LandingPageForm()
    if form.validate_on_submit():
        path = form.custom_path.data.strip().lower().replace(" ", "-")
        generated_pages[path] = {
            "heading1": form.heading1.data,
            "paragraph1": form.paragraph1.data,
            "heading2": form.heading2.data,
            "paragraph2": form.paragraph2.data
        }
        return redirect(f"/{path}")
    return render_template("generate_form.html", form=form)

@app.route("/<custom_path>", methods=["GET", "POST"])
def dynamic_page(custom_path):
    data = generated_pages.get(custom_path)
    if not data:
        return f"<h1>Page '{custom_path}' not found.</h1>", 404

    form = ContactForm()
    if form.validate_on_submit():
        save_to_google_sheet({
            "name": form.name.data,
            "email": form.email.data,
            "phone": form.phone.data,
            "claim": form.claim.data,
            "landing": custom_path
        })
        session["show_popup"] = True
        return redirect(f"/{custom_path}")

    show_popup = session.pop("show_popup", False)
    return render_template("preview.html", form=form, show_popup=show_popup, **data)

@app.route("/create-ad", methods=["GET", "POST"])
def create_ad():
    form = AdForm()
    if form.validate_on_submit():
        filepath = generate_ad_image(
            para1=form.paragraph1.data,
            para2=form.paragraph2.data,
            sentence1="Nilges Draher LLC Attorneys are Admitted in Ohio",
            sentence2="We obtained your information from data aggregators, resume databases, or publicly available sources to identify that you currently or previously held a position with " + form.company_name.data,
            company=form.company_name.data
        )
        return send_file(filepath, as_attachment=True)
    return render_template("create_ad.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)
