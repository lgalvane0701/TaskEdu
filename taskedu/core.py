"""Lógica de negocio de TaskEdu: registrar, listar, terminar y filtrar tareas."""
import json
import os
from datetime import date

PENDIENTE = "Pendiente"
TERMINADA = "Terminada"
FILTROS = {"Todas": None, "Pendientes": PENDIENTE, "Terminadas": TERMINADA}


class TaskManager:
    def __init__(self, path="tasks.json"):
        self.path = path
        self.tasks = self._load()

    # --- persistencia ---
    def _load(self):
        if not os.path.exists(self.path):
            return []
        with open(self.path, encoding="utf-8") as f:
            return json.load(f)

    def _save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=2)

    # --- HU-01 ---
    @staticmethod
    def _validate(title, subject, due):
        if not title or not title.strip():
            raise ValueError("El título no puede estar vacío.")
        if not subject or not subject.strip():
            raise ValueError("La asignatura es obligatoria.")
        try:
            date.fromisoformat(due)
        except (TypeError, ValueError):
            raise ValueError("La fecha debe tener formato AAAA-MM-DD.")

    def _next_id(self):
        return max((t["id"] for t in self.tasks), default=0) + 1

    def add(self, title, subject, due):
        self._validate(title, subject, due)
        task = {
            "id": self._next_id(),
            "title": title.strip(),
            "subject": subject.strip(),
            "due": due,
            "status": PENDIENTE,
        }
        self.tasks.append(task)
        self._save()
        return task

    # --- HU-02 / HU-04 ---
    def list(self, filtro="Todas"):
        estado = FILTROS.get(filtro)
        if estado is None:
            return list(self.tasks)
        return [t for t in self.tasks if t["status"] == estado]

    def count(self, filtro="Todas"):
        """Cantidad de tareas que cumplen el filtro (HU-04)."""
        return len(self.list(filtro))

    # --- HU-03 ---
    def mark_done(self, task_id):
        for t in self.tasks:
            if t["id"] == task_id:
                t["status"] = TERMINADA
                self._save()
                return t
        raise KeyError(f"No existe la tarea {task_id}")
