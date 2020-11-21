from . import main
from flask import render_template, flash, redirect, url_for, session, request
from .forms import GroupForm, NameEntryForm
from ..models import Group, User
from .. import db
import random

@main.route("/<group_name>", methods=["GET"])
def index_get(group_name):
    group = Group.query.filter_by(name=group_name).first()

    if group is None:
        return redirect(url_for(".create_group"))

    if "user" in session:
        user = User.query.get(session["user"])
        if user:
            if user.group_id != group.id:
                session["user"] = ""

    return render_template("index.html", users=group.users)


@main.route("/<group_name>", methods=["POST"])
def index_post(group_name):
    form = NameEntryForm()
    form.name.data = request.form["name"] or ""

    group = Group.query.filter_by(name=group_name).first()

    if form.validate():
        name = form.name.data.strip().lower().capitalize()
        user = User.query.filter_by(group=group).filter_by(name=name).first()

        if user is not None:
            session["user"] = user.id

    return redirect( url_for(".index_get", group_name=group_name) )


@main.route("/draw/<group_name>")
def draw(group_name):
    group = Group.query.filter_by(name=group_name).first()

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

    if user in users_left:
        users_left.pop( users_left.index(user) )


    i = random.randint(0, len(users_left) - 1)
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
        
        if group_by_name:
            flash("Group already exists!")
            return redirect( url_for(".create_group"))


        names = list(set(map(lambda e : e["name"].lower().capitalize() , form.names.data)))

        group = Group(
            name = form.group_name.data,
            users = [ User(name=name) for name in names ]
            )
        
        db.session.add(group)
        db.session.commit()

        flash("Success!")
        return redirect( url_for(".index_get", group_name=group.name))

    elif len(form.errors) > 0:
        for err in form.errors.items():
            err_name, errors = err

            flash(list( errors[0].values() )[0][0] )

    return render_template("create_group.html", form=form)