import React from 'react';
import LeadCard from './LeadCard';
import { Lead } from '../../types/lead';

interface LeadListProps {
  leads: Lead[];
}

const LeadList: React.FC<LeadListProps> = ({ leads }) => {
  return (
    <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
      {leads.map((lead) => (
        <LeadCard key={lead.id} lead={lead} />
      ))}
    </div>
  );
};

export default LeadList;