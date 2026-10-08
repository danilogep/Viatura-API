"""Unidades operacionais e planos de manutenção — os cadastros que a viatura referencia."""


async def test_health_responde(client):
    response = await client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


async def test_criar_uop_devolve_201_com_id(client):
    response = await client.post("/uops/", json={"nome": "UOP 09", "municipio": "Patos"})

    assert response.status_code == 201
    assert response.json()["id"] > 0


async def test_uop_com_nome_repetido_devolve_409(client, uop):
    response = await client.post(
        "/uops/", json={"nome": uop["nome"], "municipio": "Outro município"}
    )

    assert response.status_code == 409


async def test_listar_uops(client, uop, uop_secundaria):
    response = await client.get("/uops/")

    assert response.status_code == 200
    assert {item["nome"] for item in response.json()} == {uop["nome"], uop_secundaria["nome"]}


async def test_uop_inexistente_devolve_404(client):
    assert (await client.get("/uops/9999")).status_code == 404


async def test_plano_com_nome_repetido_devolve_409(client, plano):
    response = await client.post(
        "/planos/",
        json={"nome": plano["nome"], "descricao": "Outra descrição", "valor_estimado": 10.0},
    )

    assert response.status_code == 409


async def test_plano_com_valor_zero_e_rejeitado(client):
    response = await client.post(
        "/planos/",
        json={"nome": "Plano grátis", "descricao": "Não existe almoço grátis", "valor_estimado": 0},
    )

    assert response.status_code == 422


async def test_plano_inexistente_devolve_404(client):
    assert (await client.get("/planos/9999")).status_code == 404
