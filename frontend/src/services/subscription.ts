import axios from '../utils/axios';
import { SubscriptionData, CheckoutSession } from '../types/subscription';

export const fetchSubscriptionData = async (): Promise<SubscriptionData> => {
  const response = await axios.get('/subscription');
  return response.data;
};

export const createCheckoutSession = async (planName: string): Promise<CheckoutSession> => {
  const response = await axios.post('/subscription/checkout', { planName });
  return response.data;
};