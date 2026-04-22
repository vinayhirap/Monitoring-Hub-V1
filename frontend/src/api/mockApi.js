export const getDashboardOverview = () => ({
  accounts: 3,
  resources: 128,
  alerts: { critical: 2, warning: 2 },
  regions: ["ap-south-1", "ap-south-2"]
});

export const getEC2Health = () => ([
  { id: "i-01", name: "prod-api-1", cpu: 72, status: "critical" },
  { id: "i-02", name: "prod-api-2", cpu: 45, status: "ok" },
  { id: "i-03", name: "uat-app-1", cpu: 65, status: "warning" }
]);