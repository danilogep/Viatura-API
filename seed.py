import asyncio
import random
import string

from contrib.database import async_session, engine
from contrib.models import Base
from plano_manutencao.models import PlanoDeManutencaoModel
from unidade_operacional.models import UnidadeOperacionalModel
from viatura.models import ViaturaModel
from viatura.schemas import StatusViatura

# --- DADOS PARA O SORTEIO ---
CORES = ["Branca", "Preta", "Prata", "Azul", "Vermelha", "Cinza", "Caracterizada"]

# Distribuicao proxima de uma frota real: a maioria rodando, uma parcela em
# oficina e um residuo ja baixado. Sem isso o painel abre com tudo em operacao
# e os indicadores de manutencao e de baixa nunca sao exercitados.
STATUS_SORTEIO = (
    [StatusViatura.OPERACAO.value] * 7
    + [StatusViatura.MANUTENCAO.value] * 2
    + [StatusViatura.BAIXADA.value]
)

# Lista de tuplas (Marca, Modelo)
FROTA_MODELOS = [
    ("Chevrolet", "Trailblazer"),
    ("Chevrolet", "Cruze"),
    ("Nissan", "Frontier"),
    ("Toyota", "Corolla"),
    ("Toyota", "Hilux"),
    ("Renault", "Duster"),
    ("Renault", "Fluence"),
    ("Ford", "Ranger"),
    ("Mitsubishi", "L200 Triton"),
    ("Volkswagen", "Amarok")
]

# --- FUNÇÕES AUXILIARES ---
def gerar_placa():
    """Gera uma placa no padrão Mercosul (LLL1L11)"""
    letras = string.ascii_uppercase
    numeros = string.digits
    
    # Ex: ABC1D23
    p1 = ''.join(random.choices(letras, k=3))
    p2 = random.choice(numeros)
    p3 = random.choice(letras)
    p4 = ''.join(random.choices(numeros, k=2))
    
    return f"{p1}{p2}{p3}{p4}"

async def popular_banco():
    print("Semeando o banco com 50 viaturas...")
    
    # Recria as tabelas para garantir que não haja duplicidade
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("  banco limpo e recriado")

    async with async_session() as session:
        # 1. Criar Unidades Operacionais (UOPs)
        print("  criando 5 unidades operacionais")
        uops = [
            UnidadeOperacionalModel(nome="UOP 01 - João Pessoa (Sede)", municipio="João Pessoa"),
            UnidadeOperacionalModel(nome="UOP 02 - Campina Grande", municipio="Campina Grande"),
            UnidadeOperacionalModel(nome="UOP 03 - Patos", municipio="Patos"),
            UnidadeOperacionalModel(nome="UOP 04 - Cajazeiras", municipio="Cajazeiras"),
            UnidadeOperacionalModel(nome="UOP 05 - Mamanguape", municipio="Mamanguape"),
        ]
        session.add_all(uops)
        await session.commit()
        
        # Recarregar para ter os IDs disponíveis
        for u in uops:
            await session.refresh(u)

        # 2. Criar Planos de Manutenção
        print("  criando 4 planos de manutencao")
        planos = [
            PlanoDeManutencaoModel(nome="Preventiva Básica (10k)", descricao="Troca de óleo e filtros.", valor_estimado=450.00),
            PlanoDeManutencaoModel(nome="Corretiva Freios", descricao="Manutenção do sistema de frenagem.", valor_estimado=1200.00),
            PlanoDeManutencaoModel(nome="Revisão Pesada 4x4", descricao="Suspensão, tração e pneus.", valor_estimado=3500.00),
            PlanoDeManutencaoModel(nome="Blindagem e Vidros", descricao="Manutenção específica de blindados.", valor_estimado=5000.00),
        ]
        session.add_all(planos)
        await session.commit()
        
        for p in planos:
            await session.refresh(p)

        # 3. Gerar 50 Viaturas Aleatórias
        print("  criando 50 viaturas")
        viaturas = []
        placas_geradas = set()

        while len(viaturas) < 50:
            marca, modelo = random.choice(FROTA_MODELOS)
            placa = gerar_placa()
            
            if placa in placas_geradas:
                continue
            placas_geradas.add(placa)

            nova_viatura = ViaturaModel(
                placa=placa,
                marca=marca,
                modelo=modelo,
                cor=random.choice(CORES),
                ano_fabricacao=random.randint(2018, 2024),
                status=random.choice(STATUS_SORTEIO),
                unidade_operacional_id=random.choice(uops).id,
                plano_manutencao_id=random.choice(planos).id
            )
            viaturas.append(nova_viatura)

        session.add_all(viaturas)
        await session.commit()
        
    print(f"Pronto: {len(viaturas)} viaturas inseridas.")

if __name__ == '__main__':
    asyncio.run(popular_banco())