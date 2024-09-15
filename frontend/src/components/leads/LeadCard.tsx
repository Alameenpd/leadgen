import React from 'react';
import { Lead } from '../../types/lead';

interface LeadCardProps {
  lead: Lead;
}

const LeadCard: React.FC<LeadCardProps> = ({ lead }) => {
  return (
    <div className="bg-white shadow rounded-lg overflow-hidden">
      <div className="px-4 py-5 sm:p-6">
        <h3 className="text-lg leading-6 font-medium text-gray-900">{lead.name}</h3>
        <div className="mt-2 max-w-xl text-sm text-gray-500">
          <p>{lead.email}</p>
          <p>{lead.company}</p>
          <p>{lead.position}</p>
        </div>
        <div className="mt-3 text-sm">
          <a href={lead.linkedin_url} target="_blank" rel="noopener noreferrer" className="font-medium text-indigo-600 hover:text-indigo-500">
            View LinkedIn Profile
          </a>
        </div>
      </div>
      <div className="bg-gray-50 px-4 py-4 sm:px-6">
        <button
          type="button"
          className="inline-flex items-center px-2.5 py-1.5 border border-transparent text-xs font-medium rounded shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          Add to Campaign
        </button>
      </div>
    </div>
  );
};

export default LeadCard;