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
            header=form.header.data,
            para1=form.paragraph1.data,
            para2=form.paragraph2.data,
            subtext1=form.subtext1.data,
            subtext2=form.subtext2.data,
            footer=form.footer.data,
            header_color=form.header_color.data,
            para1_color=form.para1_color.data,
            para2_color=form.para2_color.data,
            subtext_color=form.subtext_color.data,
            header_size=int(form.header_size.data),
            paragraph_size=int(form.paragraph_size.data),
            subtext_size=int(form.subtext_size.data)
        )
        return send_file(filepath, as_attachment=True)
    return render_template("create_ad.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)
