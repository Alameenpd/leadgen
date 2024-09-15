import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Campaign } from '../../types/campaign';
import { startCampaign } from '../../services/campaigns';
import { useMutation, useQueryClient } from '@tanstack/react-query';

interface CampaignCardProps {
  campaign: Campaign;
}

const CampaignCard: React.FC<CampaignCardProps> = ({ campaign }) => {
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const startMutation = useMutation(startCampaign, {
    onSuccess: () => {
      queryClient.invalidateQueries(['campaigns']);
    },
  });

  const handleStart = () => {
    startMutation.mutate(campaign.id);
  };

  return (
    <div className="bg-white shadow rounded-lg overflow-hidden">
      <div className="px-4 py-5 sm:p-6">
        <h3 className="text-lg leading-6 font-medium text-gray-900">{campaign.name}</h3>
        <div className="mt-2 max-w-xl text-sm text-gray-500">
          <p>{campaign.description}</p>
        </div>
        <div className="mt-3 flex justify-between text-sm text-gray-600">
          <span>Leads: {campaign.leads_count}</span>
          <span>Messages Sent: {campaign.messages_sent}</span>
        </div>
        <div className="mt-3 flex justify-between text-sm text-gray-600">
          <span>Start Date: {new Date(campaign.start_date).toLocaleDateString()}</span>
          <span>End Date: {new Date(campaign.end_date).toLocaleDateString()}</span>
        </div>
        <div className="mt-3 flex justify-between text-sm">
          <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full 
            ${campaign.status === 'active' ? 'bg-green-100 text-green-800' : 
              campaign.status === 'completed' ? 'bg-gray-100 text-gray-800' : 'bg-yellow-100 text-yellow-800'}`}>
            {campaign.status.charAt(0).toUpperCase() + campaign.status.slice(1)}
          </span>
          <span>Success Rate: {((campaign.messages_sent > 0 ? campaign.responses_received / campaign.messages_sent : 0) * 100).toFixed(2)}%</span>
        </div>
      </div>
      <div className="bg-gray-50 px-4 py-4 sm:px-6 flex justify-between">
        <button
          onClick={() => navigate(`/campaigns/${campaign.id}`)}
          className="inline-flex items-center px-2.5 py-1.5 border border-transparent text-xs font-medium rounded shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          View Details
        </button>
        <button
          onClick={() => navigate(`/campaigns/${campaign.id}/edit`)}
          className="inline-flex items-center px-2.5 py-1.5 border border-transparent text-xs font-medium rounded shadow-sm text-white bg-yellow-600 hover:bg-yellow-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-yellow-500"
        >
          Edit
        </button>
        {campaign.status === 'draft' && (
          <button
            onClick={handleStart}
            className="inline-flex items-center px-2.5 py-1.5 border border-transparent text-xs font-medium rounded shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
          >
            Start
          </button>
        )}
      </div>
    </div>
  );
};

export default CampaignCard;