import { Box, Flex, Heading, Link, Spacer, Button } from '@chakra-ui/react';
import { Link as RouterLink } from 'react-router-dom';

const Navbar = () => {
  return (
    <Box bg="blue.600" p={4} color="white" shadow="md">
      <Flex alignItems="center" maxW="1200px" mx="auto">
        <Heading size="md" mr={8}>🚔 ViaturaAPI</Heading>
        
        <Flex gap={4}>
          <Link asChild fontWeight="bold">
            <RouterLink to="/">Dashboard</RouterLink>
          </Link>
          <Link asChild>
            <RouterLink to="/viaturas">Viaturas</RouterLink>
          </Link>
          <Link asChild>
            <RouterLink to="/uops">Unidades</RouterLink>
          </Link>
          <Link asChild>
            <RouterLink to="/planos">Planos</RouterLink>
          </Link>
        </Flex>

        <Spacer />
        
        {/* Na v3, usamos variant="surface" ou "outline" para botões secundários */}
        <Button variant="surface" size="sm">Sair</Button>
      </Flex>
    </Box>
  );
};

export default Navbar;