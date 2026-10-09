"""Previsão orçamentária: o agregado que o painel consome.

O cálculo vive no banco justamente porque somar no cliente a página corrente dá
um número errado assim que a frota passa do tamanho da página — esse é o caso que
o último teste deste arquivo trava.
"""


async def test_frota_vazia_devolve_zeros(client):
    response = await client.get("/viaturas/previsao-orcamentaria")

    assert response.status_code == 200
    assert response.json() == {
        "total_viaturas": 0,
        "em_operacao": 0,
        "em_manutencao": 0,
        "baixadas": 0,
        "previsao_orcamentaria": 0.0,
    }


async def test_soma_os_planos_das_viaturas_cadastradas(client, payload_viatura):
    for i in range(3):
        await client.post("/viaturas/", json=payload_viatura(placa=f"ORC1A1{i}"))

    corpo = (await client.get("/viaturas/previsao-orcamentaria")).json()

    assert corpo["total_viaturas"] == 3
    assert corpo["em_operacao"] == 3
    assert corpo["previsao_orcamentaria"] == 3000.00


async def test_viatura_em_manutencao_continua_no_orcamento(client, viatura):
    await client.patch(f"/viaturas/{viatura['id']}/status", json={"status": "MANUTENCAO"})

    corpo = (await client.get("/viaturas/previsao-orcamentaria")).json()

    # Em manutenção é exatamente quando o custo se realiza: tem de continuar somando.
    assert corpo["em_manutencao"] == 1
    assert corpo["previsao_orcamentaria"] == 1000.00


async def test_viatura_baixada_sai_do_orcamento(client, payload_viatura):
    ativa = (await client.post("/viaturas/", json=payload_viatura(placa="ATI1A11"))).json()
    baixada = (await client.post("/viaturas/", json=payload_viatura(placa="BAI1A11"))).json()

    await client.patch(f"/viaturas/{baixada['id']}/status", json={"status": "BAIXADA"})

    corpo = (await client.get("/viaturas/previsao-orcamentaria")).json()

    assert corpo["total_viaturas"] == 2
    assert corpo["baixadas"] == 1
    assert corpo["em_operacao"] == 1
    assert corpo["previsao_orcamentaria"] == 1000.00, (
        f"a viatura {ativa['placa']} deveria ser a única a contar no orçamento"
    )


async def test_o_total_nao_depende_do_tamanho_da_pagina(client, payload_viatura):
    """Regressão: o painel somava o custo sobre a primeira página da listagem."""
    for i in range(12):
        await client.post("/viaturas/", json=payload_viatura(placa=f"PAG1B{i:02d}"))

    primeira_pagina = (await client.get("/viaturas/?size=5&page=1")).json()
    corpo = (await client.get("/viaturas/previsao-orcamentaria")).json()

    assert len(primeira_pagina["items"]) == 5
    assert corpo["total_viaturas"] == 12
    assert corpo["previsao_orcamentaria"] == 12000.00


async def test_a_rota_nao_colide_com_a_consulta_por_id(client):
    """`/viaturas/previsao-orcamentaria` tem de ser resolvida antes de `/viaturas/{id}`."""
    response = await client.get("/viaturas/previsao-orcamentaria")

    assert response.status_code == 200
    assert "previsao_orcamentaria" in response.json()
