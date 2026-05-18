import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export const getAds = () => API.get("/ads");
export const getInsights = () => API.get("/insights/summary");
export const analyzeAd = (data) => API.post("/ai/analyze-ad", data);