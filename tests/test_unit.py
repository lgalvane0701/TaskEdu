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


def test_marcar_terminada(tm):  # HU-03
    t = tm.add("Taller 1", "Matemáticas", "2026-11-05")
    assert tm.mark_done(t["id"])["status"] == TERMINADA


def test_filtrar_por_estado(tm):  # HU-04
    a = tm.add("A", "X", "2026-11-05")
    tm.add("B", "X", "2026-11-06")
    tm.mark_done(a["id"])
    assert [t["title"] for t in tm.list("Pendientes")] == ["B"]
    assert [t["title"] for t in tm.list("Terminadas")] == ["A"]
    assert len(tm.list("Todas")) == 2
