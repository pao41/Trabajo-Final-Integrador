from datetime import timedelta

from app.core.clock import now_ar, today_ar


def test_la_hora_de_argentina_esta_tres_horas_detras_de_utc():
    assert now_ar().utcoffset() == timedelta(hours=-3)


def test_la_fecha_de_hoy_coincide_con_la_hora_de_argentina():
    assert today_ar() == now_ar().date()
