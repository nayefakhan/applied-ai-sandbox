"""Tiny Flask app — applied-ai-sandbox.

Each task in tasks/ asks you to add or fix one piece. The tests in tests/
describe exactly what "done" means.
"""
from __future__ import annotations

from datetime import datetime, timezone

from flask import Flask, render_template, request, redirect, url_for


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "sandbox-not-a-real-secret"

    # In-memory store for the sandbox. Resets on every restart, which is
    # fine for practice. Real apps use a database.
    app.notes: list[dict] = []  # type: ignore[attr-defined]

    @app.route("/")
    def home():
        return render_template("home.html", notes=app.notes)

    @app.route("/notes/new", methods=["GET", "POST"])
    def new_note():
        if request.method == "POST":
            title = (request.form.get("title") or "").strip()
            body = (request.form.get("body") or "").strip()
            errors = {}
            if not title:
                errors["title"] = "Title is required"
            if not body:
                errors["body"] = "Body is required"
            if errors:
                return render_template("new_note.html", title=title, body=body, errors=errors, idx=None)
            text_color = (request.form.get("text_color") or "#000000").strip()
            app.notes.append({
                "title": title,
                "body": body,
                "tags": "",
                "created_at": datetime.now(timezone.utc),
                "text_color": text_color,
            })
            return redirect(url_for("home"))
        return render_template("new_note.html", idx=None)

    @app.route("/notes/<int:idx>/edit", methods=["GET", "POST"])
    def edit_note(idx):
        if idx >= len(app.notes):
            return redirect(url_for("home"))
        note = app.notes[idx]
        if request.method == "POST":
            title = (request.form.get("title") or "").strip()
            body = (request.form.get("body") or "").strip()
            errors = {}
            if not title:
                errors["title"] = "Title is required"
            if not body:
                errors["body"] = "Body is required"
            if errors:
                return render_template("new_note.html", title=title, body=body,
                                       errors=errors, idx=idx,
                                       text_color=note["text_color"])
            note["title"] = title
            note["body"] = body
            note["text_color"] = (request.form.get("text_color") or "#000000").strip()
            return redirect(url_for("home"))
        return render_template("new_note.html", title=note["title"], body=note["body"],
                               text_color=note["text_color"], idx=idx)

    # TASK 02 will add a /notes/<idx>/delete route here.

    return app


if __name__ == "__main__":
    create_app().run(debug=True, port=5000)
