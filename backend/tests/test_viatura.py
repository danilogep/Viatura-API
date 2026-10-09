"""Cadastro, consulta e filtros de viatura."""

import pytest


async def test_cadastro_devolve_201_com_unidade_e_plano_aninhados(client, payload_viatura):
    response = await client.post("/viaturas/", json=payload_viatura())

    assert response.status_code == 201
    corpo = response.json()
    assert corpo["placa"] == "ABC1D23"
    assert corpo["status"] == "OPERACAO"
    # As relações precisam vir resolvidas na resposta: é o que prova que o
    # selectinload está no lugar e que não há lazy load pendente na sessão async.
    assert corpo["unidade_operacional"]["nome"] == "UOP 01 - Sede"
    assert corpo["plano_manutencao"]["valor_estimado"] == 1000.00


async def test_placa_duplicada_devolve_409(client, payload_viatura):
    await client.post("/viaturas/", json=payload_viatura(placa="DUP1A11"))

    response = await client.post("/viaturas/", json=payload_viatura(placa="DUP1A11"))

    assert response.status_code == 409
    assert "DUP1A11" in response.json()["detail"]


async def test_unidade_inexistente_devolve_404_explicando_o_que_faltou(client, payload_viatura):
    response = await client.post(
        "/viaturas/", json=payload_viatura(unidade_operacional_id=9999)
    )

    assert response.status_code == 404
    assert "Unidade operacional" in response.json()["detail"]


async def test_plano_inexistente_devolve_404(client, payload_viatura):
    response = await client.post("/viaturas/", json=payload_viatura(plano_manutencao_id=9999))

    assert response.status_code == 404
    assert "Plano de manutenção" in response.json()["detail"]


async def test_status_invalido_e_rejeitado_na_validacao(client, payload_viatura):
    response = await client.post("/viaturas/", json=payload_viatura(status="SUCATEADA"))

    assert response.status_code == 422


async def test_consulta_por_id_inexistente_devolve_404(client):
    response = await client.get("/viaturas/404")

    assert response.status_code == 404


async def test_consulta_por_id_devolve_a_viatura(client, viatura):
    response = await client.get(f"/viaturas/{viatura['id']}")

    assert response.status_code == 200
    assert response.json()["placa"] == viatura["placa"]


async def test_listagem_e_paginada(client, payload_viatura):
    for i in range(3):
        await client.post("/viaturas/", json=payload_viatura(placa=f"PAG1A1{i}"))

    response = await client.get("/viaturas/?size=2&page=1")

    assert response.status_code == 200
    corpo = response.json()
    assert corpo["total"] == 3
    assert len(corpo["items"]) == 2


@pytest.mark.parametrize(
    ("filtro", "esperado"),
    [
        ("modelo=trail", 1),  # ilike: a busca não depende da caixa
        ("modelo=hilux", 1),
        ("modelo=inexistente", 0),
        ("placa=FIL1A01", 1),
        ("status=MANUTENCAO", 0),
    ],
)
async def test_filtros_da_listagem(client, payload_viatura, filtro, esperado):
    await client.post("/viaturas/", json=payload_viatura(placa="FIL1A01"))
    await client.post("/viaturas/", json=payload_viatura(placa="FIL1A02", modelo="Hilux"))

    response = await client.get(f"/viaturas/?{filtro}")

    assert response.status_code == 200
    assert response.json()["total"] == esperado


async def test_filtro_por_status_encontra_viatura_em_manutencao(client, viatura):
    await client.patch(f"/viaturas/{viatura['id']}/status", json={"status": "MANUTENCAO"})

    response = await client.get("/viaturas/?status=MANUTENCAO")

    assert response.json()["total"] == 1
