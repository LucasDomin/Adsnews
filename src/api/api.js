import axios from "axios";

const API = axios.create({
  baseURL: "/api",
});

export const getAds = () => API.get("/ads");
export const getSummary = () => API.get("/dashboard/summary");
export const getInsights = () => API.get("/insights/summary");
export const analyzeAd = (data) => API.post("/ai/analyze-ad", data);