import React from 'react';

const activities = [
  { id: 1, type: 'lead', name: 'John Doe', action: 'added to campaign', campaign: 'Summer Outreach' },
  { id: 2, type: 'campaign', name: 'Spring Newsletter', action: 'completed' },
  { id: 3, type: 'lead', name: 'Jane Smith', action: 'responded to message' },
];

const RecentActivity: React.FC = () => {
  return (
    <div className="bg-white shadow rounded-lg">
      <div className="px-4 py-5 sm:p-6">
        <h2 className="text-lg leading-6 font-medium text-gray-900">Recent Activity</h2>
        <div className="mt-4 flow-root">
          <ul className="-my-5 divide-y divide-gray-200">
            {activities.map((activity) => (
              <li key={activity.id} className="py-4">
                <div className="flex items-center space-x-4">
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 truncate">
                      {activity.name}
                    </p>
                    <p className="text-sm text-gray-500 truncate">
                      {activity.action} {activity.campaign ? `in ${activity.campaign}` : ''}
                    </p>
                  </div>
                  <div>
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      activity.type === 'lead' ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800'
                    }`}>
                      {activity.type}
                    </span>
                  </div>
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default RecentActivity;