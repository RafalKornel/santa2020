from . import main
from flask import render_template, flash, redirect, url_for, session, request, Response
from .forms import GroupForm, NameEntryForm
from ..models import Group, User
from .. import db
import random

@main.route("/<key>", methods=["GET"])
def index_get(key):
    group = Group.query.filter_by(key=key).first()
    if group is None:
        return redirect(url_for(".create_group"))
    return render_template("index.html", users=group.users)


@main.route("/<key>", methods=["POST"])
def index_post(key):
    form = NameEntryForm()
    form.name.data = request.form["name"]
    if form.validate():
        name = form.name.data.strip().lower().capitalize()
        user = User.query.filter_by(name=name).first()

        if user is not None:
            session["user"] = user.id

    return redirect( url_for(".index_get", key=key) )


@main.route("/draw/<key>")
def draw(key):
    group = Group.query.filter_by(key=key).first()

    if group is None:
        return "Group not found", 400
    
    if session["user"] is None:
        return "User not logged", 400

    user = User.query.get(session["user"])

    if user is None:
        return "User not logged (try clearing cache)", 400

    if user.drafted:
        return {"name": User.query.get(user.drafted_person_id).name}, 200

    users_left = User.query.filter_by(group=group).filter_by(was_drafted=False).all()

    i = random.randint(0, len(users_left))
    drafted_user = users_left[i]
    drafted_user.was_drafted = True
    db.session.add(drafted_user)

    user.drafted_person_id = drafted_user.id
    user.drafted = True
    db.session.add(user)

    db.session.commit()

    return {"name": drafted_user.name}, 200
    

@main.route("/", methods=["GET", "POST"])
def create_group():
    form = GroupForm()
    
    if form.validate_on_submit():
        group_by_name = Group.query.filter_by(name=form.group_name.data).first()
        group_by_key  = Group.query.filter_by(key=form.key.data).first()
        
        if group_by_name or group_by_key:
            flash("Group already exists!")
            return redirect( url_for(".create_group"))


        names = list(set(map(lambda e : e["name"].lower().capitalize() , form.names.data)))

        group = Group(
            name = form.group_name.data,
            key = form.key.data,
            users = [ User(name=name) for name in names ]
            )
        
        db.session.add(group)
        db.session.commit()

        flash("Success!")
        return redirect( url_for(".index", key=group.key))

    elif len(form.errors) > 0:
        for err in form.errors.items():
            err_name, errors = err

            flash(list( errors[0].values() )[0][0] )

    return render_template("create_group.html", form=form)


@main.route("/test1")
def test():
    session["logged"] = "true";

    return "ok"