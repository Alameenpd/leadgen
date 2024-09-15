import React from 'react';
import { useQuery } from '@tanstack/react-query';
import CampaignList from '../components/campaigns/CampaignList';
import CampaignForm from '../components/campaigns/CampaignForm';
import { fetchCampaigns } from '../services/campaigns';

const CampaignsPage: React.FC = () => {
  const { data: campaigns, isLoading, isError } = useQuery(['campaigns'], fetchCampaigns);

  return (
    <div className="space-y-6">
      <div className="sm:flex sm:items-center sm:justify-between">
        <h1 className="text-2xl font-semibold text-gray-900">Campaigns</h1>
        <div className="mt-3 sm:mt-0 sm:ml-4">
          <CampaignForm />
        </div>
      </div>
      {isLoading ? (
        <p>Loading campaigns...</p>
      ) : isError ? (
        <p>Error fetching campaigns</p>
      ) : (
        <CampaignList campaigns={campaigns || []} />
      )}
    </div>
  );
};

export default CampaignsPage;