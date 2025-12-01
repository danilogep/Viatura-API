import { useEffect, useState } from 'react';
import { Box, Heading, Text, SimpleGrid, Card, Stat, Skeleton, Icon, Flex } from '@chakra-ui/react';
import api from '../services/api';
import type { Viatura } from '../types';
import { FaCar, FaMoneyBillWave, FaServer } from 'react-icons/fa';

const Home = () => {
  const [totalViaturas, setTotalViaturas] = useState(0);
  const [custoTotal, setCustoTotal] = useState(0);
  const [viaturasManutencao, setViaturasManutencao] = useState(0);
  const [loading, setLoading] = useState(true);

  const formatarMoeda = (valor: number) => {
    return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(valor);
  };

  useEffect(() => {
    const fetchDados = async () => {
      try {
        // CORREÇÃO: Mudamos de size=1000 para size=100 para respeitar o limite da API
        const response = await api.get('/viaturas/?size=100');
        const lista: Viatura[] = response.data.items;
        
        setTotalViaturas(response.data.total);
        
        // Conta quantas estão na oficina
        const emManutencao = lista.filter(v => v.status === 'MANUTENCAO').length;
        setViaturasManutencao(emManutencao);
        
        // Soma o custo estimado
        const total = lista.reduce((acc, v) => acc + (v.plano_manutencao?.valor_estimado || 0), 0);
        setCustoTotal(total);
      } catch (error) {
        console.error("Erro ao carregar dashboard:", error);
      } finally {
        setTimeout(() => setLoading(false), 500);
      }
    };
    fetchDados();
  }, []);

  return (
    <Box maxW="1200px" mx="auto" mt={8} p={4}>
      <Heading mb={2} color="gray.700">Painel de Controle</Heading>
      <Text color="gray.500" mb={8}>Visão estratégica da frota em tempo real.</Text>
      
      <SimpleGrid columns={{ base: 1, md: 3 }} gap={6}>
        
        {/* CARD 1: FROTA */}
        <Card.Root borderTopWidth="4px" borderColor="blue.500" shadow="md" bg="white">
          <Card.Body>
            <Stat.Root>
                <Flex align="center" justify="space-between" mb={2}>
                   <Stat.Label color="gray.500">Frota Ativa</Stat.Label>
                   <Icon as={FaCar} color="blue.200" fontSize="2xl" />
                </Flex>
                <Skeleton loading={loading} height="40px" width="100px" my={2}>
                    <Stat.ValueText fontSize="4xl" fontWeight="bold" color="blue.600">
                    {totalViaturas}
                    </Stat.ValueText>
                </Skeleton>
                <Stat.HelpText>Veículos operacionais</Stat.HelpText>
            </Stat.Root>
          </Card.Body>
        </Card.Root>

        {/* CARD 2: CUSTOS */}
        <Card.Root borderTopWidth="4px" borderColor="red.500" shadow="md" bg="white">
          <Card.Body>
            <Stat.Root>
                <Flex align="center" justify="space-between" mb={2}>
                   <Stat.Label color="gray.500">Previsão de Gastos</Stat.Label>
                   <Icon as={FaMoneyBillWave} color="red.200" fontSize="2xl" />
                </Flex>
                <Skeleton loading={loading} height="40px" width="180px" my={2}>
                    <Stat.ValueText fontSize="4xl" fontWeight="bold" color="red.600">
                    {formatarMoeda(custoTotal)}
                    </Stat.ValueText>
                </Skeleton>
                <Stat.HelpText>Ciclo de manutenção atual</Stat.HelpText>
            </Stat.Root>
          </Card.Body>
        </Card.Root>

        {/* CARD 3: STATUS */}
        <Card.Root borderTopWidth="4px" borderColor={viaturasManutencao > 0 ? "orange.500" : "green.500"} shadow="md" bg="white">
          <Card.Body>
            <Stat.Root>
                <Flex align="center" justify="space-between" mb={2}>
                   <Stat.Label color="gray.500">Em Manutenção</Stat.Label>
                   <Icon as={FaServer} color={viaturasManutencao > 0 ? "orange.200" : "green.200"} fontSize="2xl" />
                </Flex>
                <Skeleton loading={loading} height="40px" width="150px" my={2}>
                    <Stat.ValueText fontSize="4xl" mt={2} color={viaturasManutencao > 0 ? "orange.600" : "green.600"} fontWeight="bold">
                    {viaturasManutencao}
                    </Stat.ValueText>
                </Skeleton>
                <Stat.HelpText>Veículos na oficina</Stat.HelpText>
            </Stat.Root>
          </Card.Body>
        </Card.Root>

      </SimpleGrid>
    </Box>
  );
};

export default Home;