import React from 'react';
import OverviewStats from '../components/dashboard/OverviewStats';
import RecentActivity from '../components/dashboard/RecentActivity';
import WelcomeBanner from '../components/dashboard/WelcomeBanner';

const DashboardPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <WelcomeBanner />
      <OverviewStats />
      <RecentActivity />
    </div>
  );
};

export default DashboardPage;