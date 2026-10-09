import { useEffect, useState } from 'react';
import { Box, Table, Heading, Flex, Spinner, Text, Badge, Card } from '@chakra-ui/react';
import api from '../services/api';
import type { UnidadeOperacional } from '../types';

const Uops = () => {
  const [uops, setUops] = useState<UnidadeOperacional[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Busca as UOPs do backend
    api.get('/uops/')
      .then(response => setUops(response.data))
      .catch(error => console.error("Erro ao carregar UOPs:", error))
      .finally(() => setLoading(false));
  }, []);

  return (
    <Box maxW="1200px" mx="auto" mt={8} p={4}>
      <Heading mb={2} color="gray.700">Unidades Operacionais</Heading>
      <Text color="gray.500" mb={6}>Locais de lotação e responsabilidade territorial.</Text>

      {loading ? (
        <Flex justify="center" mt={10}><Spinner size="xl" color="blue.500" /></Flex>
      ) : (
        <Card.Root shadow="sm" bg="white">
          <Box overflowX="auto">
            <Table.Root interactive striped>
              <Table.Header bg="gray.50">
                <Table.Row>
                  <Table.ColumnHeader w="100px">ID</Table.ColumnHeader>
                  <Table.ColumnHeader>Nome da Unidade</Table.ColumnHeader>
                  <Table.ColumnHeader>Município/Sede</Table.ColumnHeader>
                  <Table.ColumnHeader>Status</Table.ColumnHeader>
                </Table.Row>
              </Table.Header>
              <Table.Body>
                {uops.map((uop) => (
                  <Table.Row key={uop.id}>
                    <Table.Cell fontWeight="bold" color="gray.600">#{uop.id}</Table.Cell>
                    <Table.Cell fontWeight="medium" fontSize="md">{uop.nome}</Table.Cell>
                    <Table.Cell>{uop.municipio}</Table.Cell>
                    <Table.Cell>
                        <Badge colorPalette="green" variant="subtle">Ativa</Badge>
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

export default Uops;