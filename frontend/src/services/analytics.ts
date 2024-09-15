import axios from '../utils/axios';
import { AnalyticsData } from '../types/analytics';

export const fetchAnalyticsData = async (): Promise<AnalyticsData> => {
  const response = await axios.get('/analytics');
  return response.data;
};