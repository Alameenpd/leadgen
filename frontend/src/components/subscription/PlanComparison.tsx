import React from 'react';
import { Plan } from '../../types/subscription';

interface PlanComparisonProps {
  plans: Plan[];
  currentPlan: string;
}

const PlanComparison: React.FC<PlanComparisonProps> = ({ plans, currentPlan }) => {
  return (
    <div className="bg-white shadow rounded-lg overflow-hidden">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Feature</th>
            {plans.map(plan => (
              <th key={plan.name} className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                {plan.name}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          <tr>
            <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">Price</td>
            {plans.map(plan => (
              <td key={plan.name} className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                ${plan.price}/month
              </td>
            ))}
          </tr>
          <tr>
            <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">Lead Limit</td>
            {plans.map(plan => (
              <td key={plan.name} className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {plan.leadLimit} leads/month
              </td>
            ))}
          </tr>
          <tr>
            <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">Campaign Limit</td>
            {plans.map(plan => (
              <td key={plan.name} className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {plan.campaignLimit} active campaigns
              </td>
            ))}
          </tr>
          <tr>
            <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">Message Limit</td>
            {plans.map(plan => (
              <td key={plan.name} className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {plan.messageLimit} messages/month
              </td>
            ))}
          </tr>
          {/* Add more rows for additional features */}
        </tbody>
      </table>
    </div>
  );
};

export default PlanComparison;