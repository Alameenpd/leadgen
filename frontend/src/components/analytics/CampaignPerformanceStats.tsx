import React from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
import { CampaignPerformanceData } from '../../types/analytics';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

interface CampaignPerformanceChartProps {
  data: CampaignPerformanceData[];
}

const CampaignPerformanceChart: React.FC<CampaignPerformanceChartProps> = ({ data }) => {
  const chartData = {
    labels: data.map(item => item.name),
    datasets: [
      {
        label: 'Messages Sent',
        data: data.map(item => item.messages_sent),
        backgroundColor: 'rgba(54, 162, 235, 0.6)',
      },
      {
        label: 'Responses Received',
        data: data.map(item => item.responses_received),
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
      },
    ],
  };

  const options = {
    responsive: true,
    scales: {
      x: {
        stacked: true,
      },
      y: {
        stacked: true,
      },
    },
  };

  return (
    <div className="bg-white shadow rounded-lg p-6">
      <h2 className="text-xl font-semibold text-gray-900 mb-4">Campaign Performance</h2>
      <Bar data={chartData} options={options} />
    </div>
  );
};

export default CampaignPerformanceChart;