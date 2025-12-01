import { useEffect, useState } from 'react';
import { Box, Table, Heading, Flex, Spinner, Text, Badge, Card } from '@chakra-ui/react';
import api from '../services/api';
import type { PlanoManutencao } from '../types';

const Planos = () => {
  const [planos, setPlanos] = useState<PlanoManutencao[]>([]);
  const [loading, setLoading] = useState(true);

  const formatarMoeda = (valor: number) => {
    return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(valor);
  };

  useEffect(() => {
    api.get('/planos/')
      .then(response => setPlanos(response.data))
      .catch(error => console.error(error))
      .finally(() => setLoading(false));
  }, []);

  return (
    <Box maxW="1200px" mx="auto" mt={8} p={4}>
      <Heading mb={2} color="gray.700">Planos de Manutenção</Heading>
      <Text color="gray.500" mb={6}>Tabela referencial de custos para serviços mecânicos.</Text>

      {loading ? (
        <Flex justify="center" mt={10}><Spinner size="xl" color="blue.500" /></Flex>
      ) : (
        <Card.Root shadow="sm" bg="white">
          <Box overflowX="auto">
            <Table.Root interactive>
              <Table.Header bg="gray.50">
                <Table.Row>
                  <Table.ColumnHeader w="80px">ID</Table.ColumnHeader>
                  <Table.ColumnHeader>Nome do Plano</Table.ColumnHeader>
                  <Table.ColumnHeader>Descrição Técnica</Table.ColumnHeader>
                  <Table.ColumnHeader textAlign="right">Custo Estimado</Table.ColumnHeader>
                </Table.Row>
              </Table.Header>
              <Table.Body>
                {planos.map((plano) => (
                  <Table.Row key={plano.id}>
                    <Table.Cell color="gray.500">#{plano.id}</Table.Cell>
                    <Table.Cell fontWeight="bold" color="blue.700">{plano.nome}</Table.Cell>
                    <Table.Cell color="gray.600" maxW="400px" truncate>{plano.descricao}</Table.Cell>
                    <Table.Cell textAlign="right">
                      <Badge colorPalette="green" variant="solid" fontSize="0.95em" px={2} py={1}>
                          {formatarMoeda(plano.valor_estimado)}
                      </Badge>
                    </Table.Cell>
                  </Table.Row>
                ))}
              </Table.Body>
            </Table.Root>
          </Box>
        </Card.Root>
      )}
    </Box>
  );
};

export default Planos;