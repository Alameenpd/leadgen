export interface Campaign {
    id: string;
    name: string;
    description: string;
    start_date: string;
    end_date: string;
    leads_count: number;
    messages_sent: number;
    status: 'draft' | 'active' | 'completed';
    created_at: string;
    updated_at: string;
  }
  
  export interface CreateCampaignData {
    name: string;
    description: string;
    start_date: string;
    end_date: string;
  }