import React, { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { searchLeads } from '../../services/leads';

const LeadSearchForm: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const queryClient = useQueryClient();

  const mutation = useMutation(searchLeads, {
    onSuccess: () => {
      queryClient.invalidateQueries(['leads']);
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    mutation.mutate(searchQuery);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="search" className="block text-sm font-medium text-gray-700">
          Search Leads
        </label>
        <div className="mt-1 flex rounded-md shadow-sm">
          <input
            type="text"
            name="search"
            id="search"
            className="focus:ring-indigo-500 focus:border-indigo-500 flex-1 block w-full rounded-none rounded-l-md sm:text-sm border-gray-300"
            placeholder="Enter keywords, job titles, or companies"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
          <button
            type="submit"
            className="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-r-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            Search
          </button>
        </div>
      </div>
    </form>
  );
};

export default LeadSearchForm;