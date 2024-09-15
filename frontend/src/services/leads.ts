import axios from '../utils/axios';
import { Lead } from '../types/lead';

export const fetchLeads = async (): Promise<Lead[]> => {
  const response = await axios.get('/leads');
  return response.data;
};

export const searchLeads = async (query: string): Promise<Lead[]> => {
  const response = await axios.get(`/leads/search?q=${encodeURIComponent(query)}`);
  return response.data;
};

export const addLeadToCampaign = async (leadId: string, campaignId: string): Promise<void> => {
  await axios.post(`/leads/${leadId}/campaigns/${campaignId}`);
};