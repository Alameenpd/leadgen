import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { fetchAnalyticsData } from '../../services/analytics';
import OverallStats from '../components/analytics/OverallStats';
import LeadSourceChart from '../components/analytics/LeadSourceChart';
import CampaignPerformanceChart from '../components/analytics/CampaignPerformanceChart';
import MessageSuccessRateChart from '../components/analytics/MessageSuccessRateChart';

const AnalyticsPage: React.FC = () => {
  const { data: analyticsData, isLoading, isError } = useQuery(['analytics'], fetchAnalyticsData);

  if (isLoading) return <div>Loading analytics data...</div>;
  if (isError) return <div>Error fetching analytics data</div>;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold text-gray-900">Analytics Dashboard</h1>
      
      <OverallStats stats={analyticsData.overallStats} />
      
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <LeadSourceChart data={analyticsData.leadSourceData} />
        <CampaignPerformanceChart data={analyticsData.campaignPerformanceData} />
      </div>
      
      <MessageSuccessRateChart data={analyticsData.messageSuccessRateData} />
    </div>
  );
};

export default AnalyticsPage;