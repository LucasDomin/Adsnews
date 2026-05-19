import axios from "axios";

// Em dev usa proxy do Vite. Em produção aponta pro Render.
const BASE = import.meta.env.VITE_API_URL || "";

const API = axios.create({ baseURL: BASE });

export const getAds = () => API.get("/ads/");
export const getSummary = () => API.get("/dashboard/summary");
export const analyzeAd = (data) => API.post("/ai/analyze", data);