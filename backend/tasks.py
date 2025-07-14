from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from models import (
    add_task,
    get_pending_tasks,
    get_completed_tasks,
    mark_task_complete,
    delete_task,
    rename_task
)

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        title = request.form['title']
        add_task(session['user_id'], title)

    pending = get_pending_tasks(session['user_id'])
    completed = get_completed_tasks(session['user_id'])

    return render_template('dashboard.html', pending=pending, completed=completed)

@tasks_bp.route('/complete/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    mark_task_complete(task_id, session['user_id'])
    flash('Task marked as completed.')
    return redirect(url_for('tasks.dashboard'))

@tasks_bp.route('/delete/<int:task_id>', methods=['POST'])
def delete_task_route(task_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    delete_task(task_id, session['user_id'])
    flash('Task deleted successfully.')
    return redirect(url_for('tasks.dashboard'))

@tasks_bp.route('/edit/<int:task_id>', methods=['POST'])
def edit_task(task_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    new_title = request.form['new_title']
    rename_task(task_id, new_title, session['user_id'])
    flash(f'Task renamed to: {new_title}')
    return redirect(url_for('tasks.dashboard'))
