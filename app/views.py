from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import current_user, login_required
import json
from .models import Notes
from . import db

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        content = request.form.get('note')

        if len(content) < 1:
            flash("Please type something in your note", category="error")

        else:
            new_note = Notes(content=content, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()

            flash("Note created", category="success")

    return render_template('home.html', user=current_user)


@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    data = json.loads(request.data)
    noteId = data['noteId']
    note = Notes.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            flash("Note deleted", category="success")
            return jsonify({})

    flash("Error deleting note", category="error")
    return jsonify({})
