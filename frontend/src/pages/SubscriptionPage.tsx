import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { fetchSubscriptionData } from '../../services/subscription';
import CurrentPlan from '../components/subscription/CurrentPlan';
import PlanComparison from '../components/subscription/PlanComparison';
import UpgradeButton from '../components/subscription/UpgradeButton';

const SubscriptionPage: React.FC = () => {
  const { data: subscriptionData, isLoading, isError } = useQuery(['subscription'], fetchSubscriptionData);

  if (isLoading) return <div>Loading subscription data...</div>;
  if (isError) return <div>Error fetching subscription data</div>;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold text-gray-900">Subscription Management</h1>
      
      <CurrentPlan plan={subscriptionData.currentPlan} />
      
      <PlanComparison plans={subscriptionData.availablePlans} currentPlan={subscriptionData.currentPlan} />
      
      {subscriptionData.currentPlan !== 'enterprise' && (
        <UpgradeButton currentPlan={subscriptionData.currentPlan} />
      )}
    </div>
  );
};

export default SubscriptionPage;