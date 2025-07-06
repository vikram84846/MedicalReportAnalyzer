import { useQuery } from '@tanstack/react-query';
import { api } from '@/lib/api';

export const useHealthCheck = () => {
  return useQuery({
    queryKey: ['health'],
    queryFn: api.healthCheck,
    refetchInterval: 30000, // Check every 30 seconds
    retry: 3,
    retryDelay: 1000,
  });
}; 