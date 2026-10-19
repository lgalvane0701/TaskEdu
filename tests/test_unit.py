import pytest
from taskedu.core import TaskManager, PENDIENTE, TERMINADA


@pytest.fixture
def tm(tmp_path):
    return TaskManager(str(tmp_path / "t.json"))


def test_registrar_tarea_valida(tm):  # HU-01
    t = tm.add("Taller 1", "Matemáticas", "2026-11-05")
    assert t["status"] == PENDIENTE and len(tm.list()) == 1


def test_titulo_vacio_rechazado(tm):  # HU-01
    with pytest.raises(ValueError):
        tm.add("   ", "Matemáticas", "2026-11-05")


def test_fecha_invalida_rechazada(tm):  # HU-01
    with pytest.raises(ValueError):
        tm.add("Taller 1", "Matemáticas", "05-11-2026")


def test_asignatura_obligatoria(tm):  # HU-01
    with pytest.raises(ValueError):
        tm.add("Taller 1", "  ", "2026-11-05")


def test_listar_varias_tareas(tm):  # HU-02
    tm.add("A", "X", "2026-11-05")
    tm.add("B", "Y", "2026-11-06")
    assert len(tm.list()) == 2
    assert [t["title"] for t in tm.list()] == ["A", "B"]


def test_marcar_terminada(tm):  # HU-03
    t = tm.add("Taller 1", "Matemáticas", "2026-11-05")
    assert tm.mark_done(t["id"])["status"] == TERMINADA


def test_estado_persiste_en_disco(tmp_path):  # HU-03
    path = str(tmp_path / "t.json")
    primero = TaskManager(path)
    t = primero.add("Taller 1", "Matemáticas", "2026-11-05")
    primero.mark_done(t["id"])
    # nueva instancia leyendo el mismo archivo (simula "actualizar la app")
    segundo = TaskManager(path)
    assert segundo.list("Terminadas")[0]["status"] == TERMINADA


def test_filtrar_sin_tareas(tm):  # HU-04
    assert tm.list("Pendientes") == []
    assert tm.list("Terminadas") == []
    assert tm.count("Todas") == 0


def test_filtrar_por_estado(tm):  # HU-04
    a = tm.add("A", "X", "2026-11-05")
    tm.add("B", "X", "2026-11-06")
    tm.mark_done(a["id"])
    assert [t["title"] for t in tm.list("Pendientes")] == ["B"]
    assert [t["title"] for t in tm.list("Terminadas")] == ["A"]
    assert len(tm.list("Todas")) == 2
