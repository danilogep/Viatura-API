import { useEffect, useState } from 'react';
import { Box, Heading, Text, SimpleGrid, Card, Stat, Skeleton, Icon, Flex } from '@chakra-ui/react';
import api from '../services/api';
import type { PrevisaoOrcamentaria } from '../types';
import { FaCar, FaMoneyBillWave, FaServer } from 'react-icons/fa';

const Home = () => {
  const [resumo, setResumo] = useState<PrevisaoOrcamentaria | null>(null);
  const [loading, setLoading] = useState(true);
  const [erro, setErro] = useState(false);

  const formatarMoeda = (valor: number) =>
    new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(valor);

  useEffect(() => {
    const fetchResumo = async () => {
      try {
        // Os números vêm agregados do banco. A versão anterior somava o custo
        // sobre a primeira página da listagem, o que subnotificava a previsão
        // assim que a frota passava de 100 veículos.
        const { data } = await api.get<PrevisaoOrcamentaria>('/viaturas/previsao-orcamentaria');
        setResumo(data);
      } catch (error) {
        console.error('Erro ao carregar o painel:', error);
        setErro(true);
      } finally {
        setLoading(false);
      }
    };
    fetchResumo();
  }, []);

  const emManutencao = resumo?.em_manutencao ?? 0;

  return (
    <Box maxW="1200px" mx="auto" mt={8} p={4}>
      <Heading mb={2} color="gray.700">Painel de Controle</Heading>
      <Text color="gray.500" mb={8}>Visão estratégica da frota em tempo real.</Text>

      {erro && (
        <Box bg="red.50" borderWidth="1px" borderColor="red.200" borderRadius="md" p={4} mb={6}>
          <Text color="red.700" fontWeight="medium">
            Não foi possível falar com a API. Confira se o backend está no ar.
          </Text>
        </Box>
      )}

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
                    {resumo?.em_operacao ?? 0}
                    </Stat.ValueText>
                </Skeleton>
                <Stat.HelpText>
                  {resumo ? `${resumo.total_viaturas} cadastradas · ${resumo.baixadas} baixadas` : 'Veículos operacionais'}
                </Stat.HelpText>
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
                    {formatarMoeda(resumo?.previsao_orcamentaria ?? 0)}
                    </Stat.ValueText>
                </Skeleton>
                <Stat.HelpText>Ciclo de manutenção atual</Stat.HelpText>
            </Stat.Root>
          </Card.Body>
        </Card.Root>

        {/* CARD 3: STATUS */}
        <Card.Root borderTopWidth="4px" borderColor={emManutencao > 0 ? 'orange.500' : 'green.500'} shadow="md" bg="white">
          <Card.Body>
            <Stat.Root>
                <Flex align="center" justify="space-between" mb={2}>
                   <Stat.Label color="gray.500">Em Manutenção</Stat.Label>
                   <Icon as={FaServer} color={emManutencao > 0 ? 'orange.200' : 'green.200'} fontSize="2xl" />
                </Flex>
                <Skeleton loading={loading} height="40px" width="150px" my={2}>
                    <Stat.ValueText fontSize="4xl" mt={2} color={emManutencao > 0 ? 'orange.600' : 'green.600'} fontWeight="bold">
                    {emManutencao}
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
