from functools import wraps

from flask import redirect, render_template, session


def apology(message, code=400):
    """Mostra uma página de erro com a mensagem."""
    return render_template("apology.html", message=message, code=code), code


def login_required(f):
    """Bloqueia a route se o usuário não estiver logado."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function