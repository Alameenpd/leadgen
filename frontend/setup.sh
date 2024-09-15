#!/bin/bash

# Create directory structure
mkdir -p src/{components/{layout,auth,dashboard,leads,campaigns,analytics,subscription,common},pages,services,hooks,context,utils,types,styles}

# Create layout components
touch src/components/layout/{AppShell,Navbar,Sidebar,Footer}.tsx

# Create auth components
touch src/components/auth/{LoginForm,RegisterForm}.tsx

# Create dashboard components
touch src/components/dashboard/{OverviewStats,RecentActivity,WelcomeBanner}.tsx

# Create leads components
touch src/components/leads/{LeadList,LeadCard,LeadSearchForm}.tsx

# Create campaigns components
touch src/components/campaigns/{CampaignList,CampaignCard,CampaignForm}.tsx

# Create analytics components
touch src/components/analytics/{AnalyticsOverview,ConversionChart,LeadSourceChart}.tsx

# Create subscription components
touch src/components/subscription/{PlanComparison,SubscriptionStatus}.tsx

# Create common components
touch src/components/common/{Button,Input,Modal,Dropdown,Card}.tsx

# Create pages
touch src/pages/{HomePage,DashboardPage,LeadsPage,CampaignPage,AnalyticsPage,SubscriptionPage,LoginPage,RegisterPage}.tsx

# Create services
touch src/services/{api,auth,leads,campaigns,analytics}.ts

# Create hooks
touch src/hooks/{useAuth,useLeads,useCampaigns,useAnalytics}.ts

# Create context files
touch src/context/{AuthContext,SubscriptionContext}.tsx

# Create utility files
touch src/utils/{axios,formatters}.ts

# Create type definition files
touch src/types/{lead,campaign,analytics}.ts

# Create styles file
touch src/styles/index.css

# Create config files
touch .eslintrc.js .prettierrc

# Update existing files
echo "import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
})" > vite.config.ts

echo "/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          200: '#bae6fd',
          300: '#7dd3fc',
          400: '#38bdf8',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
          800: '#075985',
          900: '#0c4a6e',
        },
        secondary: {
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
          800: '#1e293b',
          900: '#0f172a',
        },
      },
      fontFamily: {
        sans: ['Inter var', 'sans-serif'],
      },
    },
  },
  plugins: [],
}" > tailwind.config.js

echo "@import 'tailwindcss/base';
@import 'tailwindcss/components';
@import 'tailwindcss/utilities';

@layer base {
  body {
    @apply bg-gray-50 text-gray-900;
  }
}

@layer components {
  .btn-primary {
    @apply px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 transition-colors duration-200;
  }
  
  .card {
    @apply bg-white rounded-lg shadow-md p-6;
  }
}" > src/styles/index.css

# Install additional dependencies
npm install react-router-dom @tanstack/react-query axios recharts framer-motion
npm install -D tailwindcss postcss autoprefixer @headlessui/react @heroicons/react
npm install -D @typescript-eslint/eslint-plugin @typescript-eslint/parser eslint eslint-plugin-react eslint-plugin-react-hooks prettier eslint-config-prettier eslint-plugin-prettier

# Initialize Tailwind CSS
npx tailwindcss init -p

echo "Setup complete! Don't forget to update your package.json scripts and configure ESLint and Prettier."