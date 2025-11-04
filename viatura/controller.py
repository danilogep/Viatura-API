from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError # <-- DESAFIO 3: Importar
from fastapi_pagination import Page, add_pagination # <-- DESAFIO 4: Importar
from fastapi_pagination.ext.sqlalchemy import paginate # <-- DESAFIO 4: Importar
from contrib.database import get_db_session

# Importando Models e Schemas necessários
from viatura.models import ViaturaModel
from viatura.schemas import ViaturaIn, ViaturaOut, ViaturaListOut
from unidade_operacional.models import UnidadeOperacionalModel # Necessário para o join
from plano_manutencao.models import PlanoDeManutencaoModel # Necessário para o join

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
        
        # O .refresh carrega os relacionamentos (unidade_operacional e plano_manutencao)
        # graças ao lazy="selectin" que definimos no model.
        
        return ViaturaOut.model_validate(nova_viatura)

    except IntegrityError as e:
        # --- DESAFIO 3: Manipular exceção de integridade ---
        # Verificamos se o erro é de violação de chave única (placa duplicada)
        if "uc_viaturas_placa" in str(e) or "viaturas_placa_key" in str(e):
            raise HTTPException(
                status_code=status.HTTP_303_SEE_OTHER, # Status 303 conforme solicitado
                detail=f"Já existe uma viatura cadastrada com a placa: {viatura_in.placa}"
            )
        else:
            # Se for outro IntegrityError, retornamos um erro genérico 409
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Erro de integridade no banco de dados."
            )
    except Exception as e:
        # Captura outros erros (ex: UOP ID ou Plano ID não existem)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Erro ao criar viatura. Verifique se os IDs da UOP e do Plano existem. Detalhe: {str(e)}"
        )


@router.get(
    '/', 
    summary='Listar todas as Viaturas (com paginação e filtros)',
    # --- DESAFIO 2: Customizar response de retorno (GET ALL) ---
    response_model=Page[ViaturaListOut] # <-- DESAFIO 4: Paginação
)
async def get_all_viaturas(
    db_session: AsyncSession = Depends(get_db_session),
    # --- DESAFIO 1: Adicionar query parameters ---
    modelo: str = Query(None, description="Filtrar por modelo da viatura"),
    placa: str = Query(None, description="Filtrar por placa da viatura")
) -> Page[ViaturaListOut]:
    """
    Retorna uma lista paginada de viaturas, com filtros opcionais.
    Utiliza o schema customizado ViaturaListOut.
    """
    
    # Montamos a query base com os joins necessários
    query = (
        select(ViaturaModel)
        .join(UnidadeOperacionalModel, ViaturaModel.unidade_operacional_id == UnidadeOperacionalModel.id)
        .join(PlanoDeManutencaoModel, ViaturaModel.plano_manutencao_id == PlanoDeManutencaoModel.id)
        .options(
            # Garantir que os relacionamentos sejam carregados para o schema
            selectinload(ViaturaModel.unidade_operacional),
            selectinload(ViaturaModel.plano_manutencao)
        )
    )

    # --- DESAFIO 1 (Continuação): Aplicando os filtros ---
    if modelo:
        query = query.where(ViaturaModel.modelo.ilike(f"%{modelo}%"))
    if placa:
        query = query.where(ViaturaModel.placa == placa)

    # --- DESAFIO 4 (Continuação): Aplicando a paginação ---
    # O 'paginate' executa a query e retorna o objeto Page
    # O `transformer` garante que o resultado seja formatado com o ViaturaListOut
    return await paginate(db_session, query, transformer=lambda items: [ViaturaListOut.model_validate(item) for item in items])


@router.get('/{id}', summary='Consultar Viatura por ID', response_model=ViaturaOut)
async def get_viatura_by_id(
    id: int, 
    db_session: AsyncSession = Depends(get_db_session)
) -> ViaturaOut:
    """
    Retorna uma viatura específica, buscada pelo ID.
    Usa o schema completo ViaturaOut.
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