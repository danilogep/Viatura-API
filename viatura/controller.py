from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError 
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from contrib.database import get_db_session

# Importando Models e Schemas necessários
from viatura.models import ViaturaModel
from viatura.schemas import ViaturaIn, ViaturaOut, ViaturaListOut
from unidade_operacional.models import UnidadeOperacionalModel 
from plano_manutencao.models import PlanoDeManutencaoModel 

# Criamos o "roteador"
router = APIRouter(prefix='/viaturas', tags=['Viaturas'])

@router.post('/', summary='Criar nova Viatura', status_code=status.HTTP_201_CREATED)
async def create_viatura(
    viatura_in: ViaturaIn, 
    db_session: AsyncSession = Depends(get_db_session)
) -> ViaturaOut:
    """
    Cria uma nova Viatura no banco de dados.
    """
    try:
        nova_viatura = ViaturaModel(**viatura_in.model_dump())
        db_session.add(nova_viatura)
        await db_session.commit()
        await db_session.refresh(nova_viatura)
        
        return ViaturaOut.model_validate(nova_viatura)

    except IntegrityError as e:
        if "uc_viaturas_placa" in str(e) or "viaturas_placa_key" in str(e):
            raise HTTPException(
                status_code=status.HTTP_303_SEE_OTHER, 
                detail=f"Já existe uma viatura cadastrada com a placa: {viatura_in.placa}"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Erro de integridade no banco de dados."
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Erro ao criar viatura. Verifique se os IDs da UOP e do Plano existem. Detalhe: {str(e)}"
        )


@router.get(
    '/', 
    summary='Listar todas as Viaturas (com paginação e filtros)',
    response_model=Page[ViaturaListOut] 
)
async def get_all_viaturas(
    db_session: AsyncSession = Depends(get_db_session),
    modelo: str = Query(None, description="Filtrar por modelo da viatura"),
    placa: str = Query(None, description="Filtrar por placa da viatura")
) -> Page[ViaturaListOut]:
    """
    Retorna uma lista paginada de viaturas, com filtros opcionais.
    """
    
    # Montamos a query base com os joins necessários
    query = (
        select(ViaturaModel)
        .join(UnidadeOperacionalModel, ViaturaModel.unidade_operacional_id == UnidadeOperacionalModel.id)
        .join(PlanoDeManutencaoModel, ViaturaModel.plano_manutencao_id == PlanoDeManutencaoModel.id)
        .options(
            # Agora o Python sabe o que é selectinload!
            selectinload(ViaturaModel.unidade_operacional),
            selectinload(ViaturaModel.plano_manutencao)
        )
    )

    if modelo:
        query = query.where(ViaturaModel.modelo.ilike(f"%{modelo}%"))
    if placa:
        query = query.where(ViaturaModel.placa == placa)

    return await paginate(db_session, query, transformer=lambda items: [ViaturaListOut.model_validate(item) for item in items])


@router.get('/{id}', summary='Consultar Viatura por ID', response_model=ViaturaOut)
async def get_viatura_by_id(
    id: int, 
    db_session: AsyncSession = Depends(get_db_session)
) -> ViaturaOut:
    """
    Retorna uma viatura específica, buscada pelo ID.
    """
    result = await db_session.execute(
        select(ViaturaModel).where(ViaturaModel.id == id)
    )
    viatura = result.scalars().first()

    if not viatura:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Viatura com ID {id} não encontrada."
        )
        
    return ViaturaOut.model_validate(viatura)