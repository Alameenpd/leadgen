import React from 'react';
import { useQuery } from '@tanstack/react-query';
import LeadList from '../components/leads/LeadList';
import LeadSearchForm from '../components/leads/LeadSearchForm';
import { fetchLeads } from '../services/leads';

const LeadsPage: React.FC = () => {
  const { data: leads, isLoading, isError } = useQuery(['leads'], fetchLeads);

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold text-gray-900">Leads</h1>
      <LeadSearchForm />
      {isLoading ? (
        <p>Loading leads...</p>
      ) : isError ? (
        <p>Error fetching leads</p>
      ) : (
        <LeadList leads={leads || []} />
      )}
    </div>
  );
};

export default LeadsPage;