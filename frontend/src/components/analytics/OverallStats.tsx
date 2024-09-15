import React from 'react';
import { OverallStats as OverallStatsType } from '../../types/analytics';

interface OverallStatsProps {
  stats: OverallStatsType;
}

const OverallStats: React.FC<OverallStatsProps> = ({ stats }) => {
  return (
    <div className="bg-white shadow rounded-lg p-6">
      <h2 className="text-xl font-semibold text-gray-900 mb-4">Overall Statistics</h2>
      <dl className="grid grid-cols-1 gap-5 sm:grid-cols-4">
        {Object.entries(stats).map(([key, value]) => (
          <div key={key} className="px-4 py-5 bg-gray-50 shadow rounded-lg overflow-hidden sm:p-6">
            <dt className="text-sm font-medium text-gray-500 truncate">
              {key.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}
            </dt>
            <dd className="mt-1 text-3xl font-semibold text-gray-900">{value}</dd>
          </div>
        ))}
      </dl>
    </div>
  );
};

export default OverallStats;