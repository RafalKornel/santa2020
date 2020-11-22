from . import main
from flask import render_template, flash, redirect, url_for, session, request
from .forms import GroupForm, NameEntryForm
from ..models import Group, User
from .. import db
from ..utilities import permutation_without_fixed_points
    

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

    return render_template("index.html", group=group)


@main.route("/<group_name>", methods=["POST"])
def index_post(group_name):
    form = NameEntryForm()
    form.name.data  = request.form["name"] or ""
    if "pin" in request.form:
        form.pin.data   = request.form["pin"]

    group = Group.query.filter_by(name=group_name).first()

    if form.validate():
        name = form.name.data.strip().lower().capitalize()

        if group.secure:
            pin = form.pin.data
            user = User.query \
                       .filter_by(group=group) \
                       .filter_by(name=name) \
                       .filter_by(pin=pin) \
                       .first()
        else:
            user = User.query \
                       .filter_by(group=group) \
                       .filter_by(name=name) \
                       .first()

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

    return User.query.get(user.drafted_person_id).name, 200
    

@main.route("/", methods=["GET", "POST"])
def create_group():
    form = GroupForm()
    
    if form.validate_on_submit():
        group_by_name = Group.query.filter_by(name=form.group_name.data).first()
        
        if group_by_name:
            flash("Group already exists!")
            return redirect( url_for(".create_group"))

        names = list(set(map(lambda e : e["name"].lower().capitalize() , form.names.data)))
        users = [ User(name=name) for name in names]

        for user in users:
            db.session.add(user)
        
        db.session.flush()

        perm = permutation_without_fixed_points( len(users) )

        for i, u in enumerate(perm):
            users[i].drafted_person_id = users[u].id

        group = Group(
            name = form.group_name.data,
            secure = form.secure.data,
            users = users,
            )

        db.session.add(group)
        db.session.commit()

        if group.secure:
            return redirect( url_for(".group_overview", group_hash=group.name_hash))

        return redirect( url_for(".index_get", group_name=group.name))

    elif len(form.errors) > 0:
        for err in form.errors.items():
            err_name, errors = err

            flash(list( errors[0].values() )[0][0] )

    return render_template("create_group.html", form=form)


@main.route("/overview/<group_hash>")
def group_overview(group_hash):
    group = Group.query.filter_by(name_hash=group_hash).first()

    if group is None:
        return redirect(url_for(".create_group"))

    return render_template("group_overview.html", group=group)