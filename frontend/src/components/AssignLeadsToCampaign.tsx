import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { fetchLeads } from '../../services/leads';
import { assignLeadsToCampaign } from '../../services/campaigns';
import { Lead } from '../../types/lead';

interface AssignLeadsToCampaignProps {
  campaignId: string;
}

const AssignLeadsToCampaign: React.FC<AssignLeadsToCampaignProps> = ({ campaignId }) => {
  const [selectedLeads, setSelectedLeads] = useState<string[]>([]);
  const queryClient = useQueryClient();

  const { data: leads, isLoading, isError } = useQuery(['leads'], fetchLeads);

  const mutation = useMutation(
    (leadIds: string[]) => assignLeadsToCampaign(campaignId, leadIds),
    {
      onSuccess: () => {
        queryClient.invalidateQueries(['campaign', campaignId]);
        setSelectedLeads([]);
      },
    }
  );

  const handleSelectLead = (leadId: string) => {
    setSelectedLeads((prev) =>
      prev.includes(leadId)
        ? prev.filter((id) => id !== leadId)
        : [...prev, leadId]
    );
  };

  const handleAssignLeads = () => {
    mutation.mutate(selectedLeads);
  };

  if (isLoading) return <div>Loading leads...</div>;
  if (isError) return <div>Error loading leads</div>;

  return (
    <div className="mt-6">
      <h2 className="text-lg font-medium text-gray-900">Assign Leads to Campaign</h2>
      <div className="mt-4 border-t border-b border-gray-200 divide-y divide-gray-200">
        {leads?.map((lead: Lead) => (
          <div key={lead.id} className="flex items-center py-4">
            <input
              type="checkbox"
              id={`lead-${lead.id}`}
              checked={selectedLeads.includes(lead.id)}
              onChange={() => handleSelectLead(lead.id)}
              className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
            />
            <label htmlFor={`lead-${lead.id}`} className="ml-3 block text-sm font-medium text-gray-700">
              {lead.name} - {lead.email}
            </label>
          </div>
        ))}
      </div>
      <div className="mt-4">
        <button
          onClick={handleAssignLeads}
          disabled={selectedLeads.length === 0}
          className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:bg-gray-300 disabled:cursor-not-allowed"
        >
          Assign Selected Leads
        </button>
      </div>
    </div>
  );
};

export default AssignLeadsToCampaign;