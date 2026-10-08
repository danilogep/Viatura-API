from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import apaginate
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from contrib.database import get_db_session
from plano_manutencao.models import PlanoDeManutencaoModel
from unidade_operacional.models import UnidadeOperacionalModel
from viatura.models import ViaturaModel
from viatura.schemas import (
    PrevisaoOrcamentariaOut,
    StatusViatura,
    ViaturaAlocacaoIn,
    ViaturaIn,
    ViaturaListOut,
    ViaturaOut,
    ViaturaStatusIn,
)

router = APIRouter(prefix='/viaturas', tags=['Viaturas'])

# As duas relações precisam vir carregadas: ViaturaOut as serializa, e em sessão
# assíncrona um lazy load fora do contexto do await estoura MissingGreenlet.
_RELACOES = (
    selectinload(ViaturaModel.unidade_operacional),
    selectinload(ViaturaModel.plano_manutencao),
)


async def _buscar_viatura(db_session: AsyncSession, id: int) -> ViaturaModel:
    result = await db_session.execute(
        select(ViaturaModel).where(ViaturaModel.id == id).options(*_RELACOES)
    )
    viatura = result.scalars().first()

    if not viatura:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Viatura com ID {id} não encontrada.",
        )

    return viatura


@router.post('/', summary='Criar nova Viatura', status_code=status.HTTP_201_CREATED)
async def create_viatura(
    viatura_in: ViaturaIn,
    db_session: AsyncSession = Depends(get_db_session),
) -> ViaturaOut:
    """Cadastra uma viatura e a aloca a uma unidade operacional.

    Uma viatura já baixada não pode ser cadastrada: baixa é saída definitiva da
    frota, e alocá-la a uma unidade a traria de volta pela porta dos fundos.
    """
    if viatura_in.status is StatusViatura.BAIXADA:
        raise HTTPException(
            status_code=422,
            detail="Não é possível cadastrar uma viatura já baixada em uma unidade operacional.",
        )

    # Validar as chaves estrangeiras antes do insert devolve um 404 explicando o
    # que faltou, em vez de um IntegrityError genérico do banco.
    for model, id_informado, rotulo in (
        (UnidadeOperacionalModel, viatura_in.unidade_operacional_id, "Unidade operacional"),
        (PlanoDeManutencaoModel, viatura_in.plano_manutencao_id, "Plano de manutenção"),
    ):
        existe = await db_session.execute(select(model.id).where(model.id == id_informado))
        if existe.scalars().first() is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{rotulo} com ID {id_informado} não encontrado.",
            )

    nova_viatura = ViaturaModel(**viatura_in.model_dump())
    db_session.add(nova_viatura)

    try:
        await db_session.commit()
    except IntegrityError:
        # Duas requisições simultâneas com a mesma placa: a segunda cai aqui, na
        # constraint do banco, que é o único ponto que consegue decidir a disputa.
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Já existe uma viatura cadastrada com a placa: {viatura_in.placa}",
        ) from None

    return ViaturaOut.model_validate(await _buscar_viatura(db_session, nova_viatura.id))


@router.get(
    '/',
    summary='Listar todas as Viaturas (com paginação e filtros)',
    response_model=Page[ViaturaListOut],
)
async def get_all_viaturas(
    db_session: AsyncSession = Depends(get_db_session),
    modelo: str | None = Query(None, description="Filtrar por modelo da viatura"),
    placa: str | None = Query(None, description="Filtrar por placa da viatura"),
    status_viatura: StatusViatura | None = Query(
        None, alias="status", description="Filtrar por situação operacional"
    ),
) -> Page[ViaturaListOut]:
    """Retorna uma lista paginada de viaturas, com filtros opcionais."""
    query = select(ViaturaModel).options(*_RELACOES)

    if modelo:
        query = query.where(ViaturaModel.modelo.ilike(f"%{modelo}%"))
    if placa:
        query = query.where(ViaturaModel.placa == placa)
    if status_viatura:
        query = query.where(ViaturaModel.status == status_viatura.value)

    return await apaginate(
        db_session,
        query,
        transformer=lambda items: [ViaturaListOut.model_validate(item) for item in items],
    )


@router.get(
    '/previsao-orcamentaria',
    summary='Previsão orçamentária e composição da frota',
    response_model=PrevisaoOrcamentariaOut,
)
async def get_previsao_orcamentaria(
    db_session: AsyncSession = Depends(get_db_session),
) -> PrevisaoOrcamentariaOut:
    """Consolida a frota e o custo previsto de manutenção.

    O cálculo é agregado no banco, e não sobre uma página de resultados: somar no
    cliente o que veio na primeira página dá um número errado assim que a frota
    passa do tamanho da página.
    """
    contagem = await db_session.execute(
        select(ViaturaModel.status, func.count()).group_by(ViaturaModel.status)
    )
    por_status = dict(contagem.all())

    previsao = await db_session.execute(
        select(func.coalesce(func.sum(PlanoDeManutencaoModel.valor_estimado), 0.0))
        .select_from(ViaturaModel)
        .join(
            PlanoDeManutencaoModel,
            ViaturaModel.plano_manutencao_id == PlanoDeManutencaoModel.id,
        )
        .where(ViaturaModel.status != StatusViatura.BAIXADA.value)
    )

    return PrevisaoOrcamentariaOut(
        total_viaturas=sum(por_status.values()),
        em_operacao=por_status.get(StatusViatura.OPERACAO.value, 0),
        em_manutencao=por_status.get(StatusViatura.MANUTENCAO.value, 0),
        baixadas=por_status.get(StatusViatura.BAIXADA.value, 0),
        previsao_orcamentaria=round(float(previsao.scalar_one()), 2),
    )


@router.get('/{id}', summary='Consultar Viatura por ID', response_model=ViaturaOut)
async def get_viatura_by_id(
    id: int,
    db_session: AsyncSession = Depends(get_db_session),
) -> ViaturaOut:
    """Retorna uma viatura específica, buscada pelo ID."""
    return ViaturaOut.model_validate(await _buscar_viatura(db_session, id))


@router.patch(
    '/{id}/status',
    summary='Alterar a situação operacional da Viatura',
    response_model=ViaturaOut,
)
async def update_status_viatura(
    id: int,
    payload: ViaturaStatusIn,
    db_session: AsyncSession = Depends(get_db_session),
) -> ViaturaOut:
    """Move a viatura entre OPERACAO, MANUTENCAO e BAIXADA.

    A baixa é irreversível pela API: reverter uma baixa é ato de patrimônio, não
    de operação, e liberar isso em um PATCH apagaria o rastro da saída do veículo.
    """
    viatura = await _buscar_viatura(db_session, id)

    if viatura.status == StatusViatura.BAIXADA.value and payload.status is not StatusViatura.BAIXADA:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Viatura baixada não retorna à frota: a baixa é definitiva.",
        )

    viatura.status = payload.status.value
    await db_session.commit()
    # expire_on_commit=False mantem os atributos carregados apos o commit, o que
    # deixaria a resposta mostrando o estado anterior. O expire forca a releitura.
    db_session.expire(viatura)

    return ViaturaOut.model_validate(await _buscar_viatura(db_session, id))


@router.patch(
    '/{id}/alocacao',
    summary='Realocar a Viatura para outra Unidade Operacional',
    response_model=ViaturaOut,
)
async def alocar_viatura(
    id: int,
    payload: ViaturaAlocacaoIn,
    db_session: AsyncSession = Depends(get_db_session),
) -> ViaturaOut:
    """Transfere a viatura para outra unidade operacional.

    Regra de negócio central do módulo: **viatura baixada não é alocada.**
    """
    viatura = await _buscar_viatura(db_session, id)

    if viatura.status == StatusViatura.BAIXADA.value:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                f"Viatura {viatura.placa} está baixada e não pode ser alocada "
                "a uma unidade operacional."
            ),
        )

    destino = await db_session.execute(
        select(UnidadeOperacionalModel.id).where(
            UnidadeOperacionalModel.id == payload.unidade_operacional_id
        )
    )
    if destino.scalars().first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unidade Operacional com ID {payload.unidade_operacional_id} não encontrada.",
        )

    viatura.unidade_operacional_id = payload.unidade_operacional_id
    await db_session.commit()
    # Sem o expire, `viatura.unidade_operacional` continuaria apontando para a
    # unidade antiga: trocar a FK nao recarrega a relacao ja materializada.
    db_session.expire(viatura)

    return ViaturaOut.model_validate(await _buscar_viatura(db_session, id))
