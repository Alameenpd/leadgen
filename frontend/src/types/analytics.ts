export interface OverallStats {
    total_leads: number;
    total_campaigns: number;
    total_messages_sent: number;
    total_responses_received: number;
  }
  
  export interface LeadSourceData {
    [source: string]: number;
  }
  
  export interface CampaignPerformanceData {
    name: string;
    messages_sent: number;
    responses_received: number;
  }
  
  export interface MessageSuccessRateData {
    date: string;
    success_rate: number;
  }
  
  export interface AnalyticsData {
    overallStats: OverallStats;
    leadSourceData: LeadSourceData;
    campaignPerformanceData: CampaignPerformanceData[];
    messageSuccessRateData: MessageSuccessRateData[];
  }