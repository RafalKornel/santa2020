from . import main
from flask import render_template, flash
from .forms import GroupForm
from ..models import Group, User
from .. import db

@main.route("/")
def index():
    return render_template("index.html")


@main.route("/create_group", methods=["GET", "POST"])
def create_group():
    form = GroupForm()
    if form.validate_on_submit():
        group_by_name = Group.query.filter_by(name=form.group_name.data).first()
        group_by_key  = Group.query.filter_by(key=form.key.data).first()
        
        if group_by_name or group_by_key:
            flash("Group already exists!")
            return render_template("create_group.html", form=form)


        names = list(set(map(lambda e : e["name"].lower().capitalize() , form.names.data)))

        group = Group(
            name = form.group_name.data,
            key = form.key.data,
            users = [ User(name=name) for name in names ]
            )
        
        db.session.add(group)
        db.session.commit()

        flash("Success!")
    elif len(form.errors) > 0:
        for err in form.errors.items():
            err_name, errors = err
            
            flash(list( errors[0].values() )[0][0] )

    return render_template("create_group.html", form=form)