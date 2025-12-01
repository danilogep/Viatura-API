import { useEffect, useState } from 'react';
import { 
  Box, Table, Heading, Badge, Button, Flex, Spinner, Input, HStack 
} from '@chakra-ui/react';
import api from '../services/api';
import type { Viatura } from '../types';
import { FaPlus } from 'react-icons/fa';

const Viaturas = () => {
  const [viaturas, setViaturas] = useState<Viatura[]>([]);
  const [loading, setLoading] = useState(true);
  const [busca, setBusca] = useState('');

  const fetchViaturas = async () => {
    try {
      const response = await api.get('/viaturas/?size=100'); 
      setViaturas(response.data.items); 
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchViaturas(); }, []);

  const viaturasFiltradas = viaturas.filter(v => 
    v.placa.toLowerCase().includes(busca.toLowerCase()) ||
    v.modelo.toLowerCase().includes(busca.toLowerCase())
  );

  const getStatusColor = (status: string) => {
    switch(status) {
        case 'OPERACAO': return 'green';
        case 'MANUTENCAO': return 'orange';
        case 'BAIXADA': return 'red';
        default: return 'gray';
    }
  };

  return (
    <Box maxW="1200px" mx="auto" mt={8} p={4}>
      <Flex justify="space-between" align="center" mb={6} wrap="wrap" gap={4}>
        <Heading size="lg" color="gray.700">Frota de Viaturas</Heading>
        <HStack>
            <Input 
                placeholder="🔍 Buscar placa..." 
                value={busca}
                onChange={(e) => setBusca(e.target.value)}
                bg="white" width="300px"
            />
            <Button colorPalette="blue"><FaPlus /> Nova</Button>
        </HStack>
      </Flex>

      {loading ? (
        <Flex justify="center" mt={10}><Spinner size="xl" color="blue.500" /></Flex>
      ) : (
        <Box overflowX="auto" shadow="md" borderRadius="lg" borderWidth="1px" bg="white">
          <Table.Root interactive striped>
            <Table.Header bg="gray.100">
              <Table.Row>
                <Table.ColumnHeader>Placa</Table.ColumnHeader>
                <Table.ColumnHeader>Modelo</Table.ColumnHeader>
                <Table.ColumnHeader>Status</Table.ColumnHeader>
                <Table.ColumnHeader>UOP</Table.ColumnHeader>
                <Table.ColumnHeader>Plano</Table.ColumnHeader>
                <Table.ColumnHeader>Ações</Table.ColumnHeader>
              </Table.Row>
            </Table.Header>
            <Table.Body>
              {viaturasFiltradas.map((v) => (
                <Table.Row key={v.id}>
                  <Table.Cell fontWeight="bold">{v.placa}</Table.Cell>
                  <Table.Cell>{v.marca} {v.modelo}</Table.Cell>
                  <Table.Cell>
                    <Badge colorPalette={getStatusColor(v.status)} variant="solid">
                        {v.status}
                    </Badge>
                  </Table.Cell>
                  <Table.Cell>{v.unidade_operacional?.nome}</Table.Cell>
                  <Table.Cell fontSize="sm">{v.plano_manutencao?.nome}</Table.Cell>
                  <Table.Cell><Button size="xs" variant="outline">Editar</Button></Table.Cell>
                </Table.Row>
              ))}
            </Table.Body>
          </Table.Root>
        </Box>
      )}
    </Box>
  );
};

export default Viaturas;