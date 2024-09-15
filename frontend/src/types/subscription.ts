export interface Plan {
    name: string;
    price: number;
    leadLimit: number;
    campaignLimit: number;
    messageLimit: number;
    additionalFeatures?: string[];
  }
  
  export interface SubscriptionData {
    currentPlan: string;
    availablePlans: Plan[];
  }
  
  export interface CheckoutSession {
    checkoutUrl: string;
  }