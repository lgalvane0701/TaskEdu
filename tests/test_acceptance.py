"""Pruebas de aceptación basadas en los criterios de HU-01 a HU-04."""
from taskedu.web import create_app


def page(c, url="/"):
    return c.get(url).get_data(as_text=True)


def test_aceptacion_hu01_hu02_hu03_hu04(tmp_path):
    c = create_app(str(tmp_path / "t.json")).test_client()
    # HU-02: sin tareas -> mensaje informativo
    assert "No hay tareas registradas" in page(c)
    # HU-01: título vacío no se acepta
    r = c.post("/agregar", data={"title": "", "subject": "Inglés", "due": "2026-11-01"},
               follow_redirects=True).get_data(as_text=True)
    assert "no puede estar vacío" in r
    # HU-01: confirmación al registrar
    r = c.post("/agregar", data={"title": "Ensayo", "subject": "Inglés", "due": "2026-11-01"},
               follow_redirects=True).get_data(as_text=True)
    assert "Tarea registrada correctamente" in r
    c.post("/agregar", data={"title": "Quiz", "subject": "Química", "due": "2026-11-02"})
    # HU-02: muestra asignatura, fecha y estado
    p = page(c)
    assert "Inglés" in p and "2026-11-01" in p and "Pendiente" in p
    # HU-03: cambia a Terminada
    c.post("/terminar/1")
    # HU-04: filtros
    assert "Ensayo" in page(c, "/?filtro=Terminadas") and "Quiz" not in page(c, "/?filtro=Terminadas")
    assert "Quiz" in page(c, "/?filtro=Pendientes") and "Ensayo" not in page(c, "/?filtro=Pendientes")
