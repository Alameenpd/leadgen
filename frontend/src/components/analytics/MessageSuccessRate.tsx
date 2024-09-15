import React from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
import { MessageSuccessRateData } from '../../types/analytics';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

interface MessageSuccessRateChartProps {
  data: MessageSuccessRateData[];
}

const MessageSuccessRateChart: React.FC<MessageSuccessRateChartProps> = ({ data }) => {
  const chartData = {
    labels: data.map(item => item.date),
    datasets: [
      {
        label: 'Success Rate',
        data: data.map(item => item.success_rate),
        fill: false,
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1,
      },
    ],
  };

  const options = {
    responsive: true,
    scales: {
      y: {
        beginAtZero: true,
        max: 100,
        ticks: {
          callback: function(value: number) {
            return value + '%';
          },
        },
      },
    },
  };

  return (
    <div className="bg-white shadow rounded-lg p-6">
      <h2 className="text-xl font-semibold text-gray-900 mb-4">Message Success Rate Over Time</h2>
      <Line data={chartData} options={options} />
    </div>
  );
};

export default MessageSuccessRateChart;