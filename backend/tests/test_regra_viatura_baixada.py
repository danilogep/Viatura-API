"""A regra de negócio central do módulo: viatura baixada não volta a ser alocada.

Baixa é saída definitiva da frota. Se a API deixasse realocar uma viatura baixada,
o veículo reapareceria no efetivo de uma unidade e voltaria a contar na previsão
orçamentária — que é exatamente o número que a baixa deveria reduzir.
"""


async def _baixar(client, viatura_id):
    response = await client.patch(f"/viaturas/{viatura_id}/status", json={"status": "BAIXADA"})
    assert response.status_code == 200, response.text
    return response.json()


async def test_cadastrar_viatura_ja_baixada_e_recusado(client, payload_viatura):
    response = await client.post("/viaturas/", json=payload_viatura(status="BAIXADA"))

    assert response.status_code == 422
    assert "baixada" in response.json()["detail"].lower()


async def test_viatura_baixada_nao_pode_ser_alocada_a_outra_unidade(
    client, viatura, uop_secundaria
):
    await _baixar(client, viatura["id"])

    response = await client.patch(
        f"/viaturas/{viatura['id']}/alocacao",
        json={"unidade_operacional_id": uop_secundaria["id"]},
    )

    assert response.status_code == 409
    assert viatura["placa"] in response.json()["detail"]

    # E a alocação original permanece intacta.
    atual = await client.get(f"/viaturas/{viatura['id']}")
    assert atual.json()["unidade_operacional"]["id"] == viatura["unidade_operacional"]["id"]


async def test_baixa_e_irreversivel_pela_api(client, viatura):
    await _baixar(client, viatura["id"])

    response = await client.patch(
        f"/viaturas/{viatura['id']}/status", json={"status": "OPERACAO"}
    )

    assert response.status_code == 409
    assert (await client.get(f"/viaturas/{viatura['id']}")).json()["status"] == "BAIXADA"


async def test_baixar_viatura_ja_baixada_e_idempotente(client, viatura):
    await _baixar(client, viatura["id"])

    # Repetir a baixa não deve explodir: é a mesma intenção, aplicada duas vezes.
    assert (await _baixar(client, viatura["id"]))["status"] == "BAIXADA"


async def test_viatura_em_manutencao_continua_alocavel(client, viatura, uop_secundaria):
    await client.patch(f"/viaturas/{viatura['id']}/status", json={"status": "MANUTENCAO"})

    response = await client.patch(
        f"/viaturas/{viatura['id']}/alocacao",
        json={"unidade_operacional_id": uop_secundaria["id"]},
    )

    assert response.status_code == 200
    assert response.json()["unidade_operacional"]["id"] == uop_secundaria["id"]


async def test_alocar_para_unidade_inexistente_devolve_404(client, viatura):
    response = await client.patch(
        f"/viaturas/{viatura['id']}/alocacao", json={"unidade_operacional_id": 9999}
    )

    assert response.status_code == 404


async def test_alterar_status_de_viatura_inexistente_devolve_404(client):
    response = await client.patch("/viaturas/9999/status", json={"status": "MANUTENCAO"})

    assert response.status_code == 404
