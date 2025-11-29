from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError # Importante para tratar erros de banco
from contrib.database import get_db_session
from plano_manutencao.models import PlanoDeManutencaoModel
from plano_manutencao.schemas import PlanoDeManutencaoIn, PlanoDeManutencaoOut

# Criamos o "roteador" que agrupará todas as rotas deste módulo
router = APIRouter(prefix='/planos', tags=['Planos de Manutenção'])

@router.post('/', summary='Criar novo Plano de Manutenção', status_code=status.HTTP_201_CREATED)
async def create_plano(
    plano_in: PlanoDeManutencaoIn, 
    db_session: AsyncSession = Depends(get_db_session)
) -> PlanoDeManutencaoOut:
    """
    Cria um novo Plano de Manutenção no banco de dados.
    """
    # Criamos o objeto modelo diretamente com os dados validados
    novo_plano = PlanoDeManutencaoModel(**plano_in.model_dump())
    
    try:
        db_session.add(novo_plano)
        await db_session.commit()
        await db_session.refresh(novo_plano)
        
        return PlanoDeManutencaoOut.model_validate(novo_plano)
        
    except IntegrityError as e:
        # Se o banco reclamar de duplicidade, capturamos aqui
        await db_session.rollback() # Desfaz a transação que falhou
        
        # Verifica se o erro é sobre a chave única de 'nome'
        if "plano_de_manutencaos_nome_key" in str(e) or "unique constraint" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Já existe um plano com o nome: {plano_in.nome}"
            )
        # Se for outro erro de integridade desconhecido
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro de integridade ao salvar o plano."
        )

@router.get('/', summary='Listar todos os Planos de Manutenção')
async def get_all_planos(
    db_session: AsyncSession = Depends(get_db_session)
) -> list[PlanoDeManutencaoOut]:
    """
    Retorna uma lista de todos os planos de manutenção.
    """
    result = await db_session.execute(select(PlanoDeManutencaoModel))
    planos = result.scalars().all()
    
    return [PlanoDeManutencaoOut.model_validate(plano) for plano in planos]

@router.get('/{id}', summary='Consultar Plano por ID')
async def get_plano_by_id(
    id: int, 
    db_session: AsyncSession = Depends(get_db_session)
) -> PlanoDeManutencaoOut:
    """
    Retorna um plano de manutenção específico, buscado pelo ID.
    """
    result = await db_session.execute(
        select(PlanoDeManutencaoModel).where(PlanoDeManutencaoModel.id == id)
    )
    plano = result.scalars().first()

    if not plano:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plano de manutenção com ID {id} não encontrado."
        )
        
    return PlanoDeManutencaoOut.model_validate(plano)