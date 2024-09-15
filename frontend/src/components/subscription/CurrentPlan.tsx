import React from 'react';
import { Plan } from '../../types/subscription';

interface CurrentPlanProps {
  plan: Plan;
}

const CurrentPlan: React.FC<CurrentPlanProps> = ({ plan }) => {
  return (
    <div className="bg-white shadow rounded-lg p-6">
      <h2 className="text-xl font-semibold text-gray-900 mb-4">Current Plan: {plan.name}</h2>
      <div className="space-y-2">
        <p><strong>Price:</strong> ${plan.price}/month</p>
        <p><strong>Lead Limit:</strong> {plan.leadLimit} leads/month</p>
        <p><strong>Campaign Limit:</strong> {plan.campaignLimit} active campaigns</p>
        <p><strong>Message Limit:</strong> {plan.messageLimit} messages/month</p>
        {plan.additionalFeatures && (
          <div>
            <strong>Additional Features:</strong>
            <ul className="list-disc list-inside ml-4">
              {plan.additionalFeatures.map((feature, index) => (
                <li key={index}>{feature}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

export default CurrentPlan;