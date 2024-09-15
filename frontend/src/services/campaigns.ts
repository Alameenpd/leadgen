import axios from '../utils/axios';
import { Campaign, CreateCampaignData } from '../types/campaign';

export const fetchCampaigns = async (): Promise<Campaign[]> => {
  const response = await axios.get('/campaigns');
  return response.data;
};

export const createCampaign = async (campaignData: CreateCampaignData): Promise<Campaign> => {
  const response = await axios.post('/campaigns', campaignData);
  return response.data;
};

export const updateCampaign = async (id: string, campaignData: Partial<CreateCampaignData>): Promise<Campaign> => {
  const response = await axios.put(`/campaigns/${id}`, campaignData);
  return response.data;
};

export const deleteCampaign = async (id: string): Promise<void> => {
  await axios.delete(`/campaigns/${id}`);
};

export const startCampaign = async (id: string): Promise<void> => {
  await axios.post(`/campaigns/${id}/start`);
};

export const fetchCampaignById = async (id: string): Promise<Campaign> => {
  const response = await axios.get(`/campaigns/${id}`);
  return response.data;
};

export const assignLeadsToCampaign = async (campaignId: string, leadIds: string[]): Promise<void> => {
  await axios.post(`/campaigns/${campaignId}/assign-leads`, { leadIds });
};