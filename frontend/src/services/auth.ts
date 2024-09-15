import axios from '../utils/axios';
import { User } from '../types/user';

interface LoginData {
  email: string;
  password: string;
}

interface AuthResponse {
  user: User;
  token: string;
}

export const login = async (data: LoginData): Promise<AuthResponse> => {
  const response = await axios.post('/auth/login', data);
  return response.data;
};

export const register = async (data: LoginData): Promise<AuthResponse> => {
  const response = await axios.post('/auth/register', data);
  return response.data;
};

export const getUser = async (): Promise<User> => {
  const response = await axios.get('/auth/user');
  return response.data;
};

export const logout = () => {
  localStorage.removeItem('token');
};