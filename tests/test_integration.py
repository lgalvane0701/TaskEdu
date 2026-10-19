from taskedu.web import create_app


def test_flujo_completo_y_persistencia(tmp_path):
    path = str(tmp_path / "t.json")
    c = create_app(path).test_client()
    c.post("/agregar", data={"title": "Informe", "subject": "Física", "due": "2026-11-10"})
    c.post("/terminar/1")
    # "Actualizar la aplicación": nueva instancia leyendo el mismo archivo
    html = create_app(path).test_client().get("/").get_data(as_text=True)
    assert "Informe" in html and "Terminada" in html
