import React from 'react';
import { useMutation } from '@tanstack/react-query';
import { createCheckoutSession } from '../../services/subscription';

interface UpgradeButtonProps {
  currentPlan: string;
}

const UpgradeButton: React.FC<UpgradeButtonProps> = ({ currentPlan }) => {
  const mutation = useMutation(createCheckoutSession, {
    onSuccess: (data) => {
      window.location.href = data.checkoutUrl;
    },
  });

  const handleUpgrade = () => {
    const nextPlan = currentPlan === 'basic' ? 'pro' : 'enterprise';
    mutation.mutate(nextPlan);
  };

  return (
    <button
      onClick={handleUpgrade}
      className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
    >
      Upgrade to {currentPlan === 'basic' ? 'Pro' : 'Enterprise'}
    </button>
  );
};

export default UpgradeButton;