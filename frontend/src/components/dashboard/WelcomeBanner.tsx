import React from 'react';

const WelcomeBanner: React.FC = () => {
  return (
    <div className="bg-white shadow rounded-lg">
      <div className="px-4 py-5 sm:p-6">
        <h1 className="text-2xl font-semibold text-gray-900">Welcome back, User!</h1>
        <p className="mt-1 text-sm text-gray-600">
          Here's what's happening with your leads and campaigns today.
        </p>
      </div>
    </div>
  );
};

export default WelcomeBanner;