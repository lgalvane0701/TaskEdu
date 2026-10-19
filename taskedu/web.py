from flask import Flask, flash, redirect, render_template, request, url_for
from .core import FILTROS, TaskManager


def create_app(path="tasks.json"):
    app = Flask(__name__)
    app.secret_key = "taskedu-dev"
    manager = TaskManager(path)

    @app.get("/")
    def index():
        filtro = request.args.get("filtro", "Todas")
        if filtro not in FILTROS:
            filtro = "Todas"
        return render_template("index.html", tasks=manager.list(filtro),
                               filtro=filtro, filtros=list(FILTROS))

    @app.post("/agregar")
    def agregar():
        try:
            manager.add(request.form.get("title"), request.form.get("subject"),
                        request.form.get("due"))
            flash("Tarea registrada correctamente.", "ok")
        except ValueError as e:
            flash(str(e), "error")
        return redirect(url_for("index"))

    @app.post("/terminar/<int:task_id>")
    def terminar(task_id):
        try:
            manager.mark_done(task_id)
            flash("Tarea marcada como terminada.", "ok")
        except KeyError:
            flash("La tarea no existe.", "error")
        return redirect(url_for("index", filtro=request.args.get("filtro", "Todas")))

    return app
