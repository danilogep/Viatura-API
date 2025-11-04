from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from contrib.database import get_db_session
from unidade_operacional.models import UnidadeOperacionalModel
from unidade_operacional.schemas import UnidadeOperacionalIn, UnidadeOperacionalOut

# Criamos o "roteador"
router = APIRouter(prefix='/uops', tags=['Unidades Operacionais'])

@router.post('/', summary='Criar nova Unidade Operacional', status_code=status.HTTP_201_CREATED)
async def create_uop(
    uop_in: UnidadeOperacionalIn, 
    db_session: AsyncSession = Depends(get_db_session)
) -> UnidadeOperacionalOut:
    """
    Cria uma nova Unidade Operacional no banco de dados.
    """
    
    # Verifica se já existe uma UOP com o mesmo nome
    result = await db_session.execute(
        select(UnidadeOperacionalModel).where(UnidadeOperacionalModel.nome == uop_in.nome)
    )
    if result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Já existe uma UOP com o nome: {uop_in.nome}"
        )

    nova_uop = UnidadeOperacionalModel(**uop_in.model_dump())
    db_session.add(nova_uop)
    await db_session.commit()
    await db_session.refresh(nova_uop)
    
    return UnidadeOperacionalOut.model_validate(nova_uop)


@router.get('/', summary='Listar todas as Unidades Operacionais')
async def get_all_uops(
    db_session: AsyncSession = Depends(get_db_session)
) -> list[UnidadeOperacionalOut]:
    """
    Retorna uma lista de todas as Unidades Operacionais.
    """
    result = await db_session.execute(select(UnidadeOperacionalModel))
    uops = result.scalars().all()
    
    return [UnidadeOperacionalOut.model_validate(uop) for uop in uops]


@router.get('/{id}', summary='Consultar Unidade Operacional por ID')
async def get_uop_by_id(
    id: int, 
    db_session: AsyncSession = Depends(get_db_session)
) -> UnidadeOperacionalOut:
    """
    Retorna uma unidade operacional específica, buscada pelo ID.
    """
    result = await db_session.execute(
        select(UnidadeOperacionalModel).where(UnidadeOperacionalModel.id == id)
    )
    uop = result.scalars().first()

    if not uop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unidade Operacional com ID {id} não encontrada."
        )
        
    return UnidadeOperacionalOut.model_validate(uop)