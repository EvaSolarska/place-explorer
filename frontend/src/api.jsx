import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({baseURL: API_BASE_URL });

export const getAllPlaces = async () => {
  const response = await api.get('/places/');
  return response.data;
};

export const getPlaceById = async (placeId) => {
  const response = await api.get(`/places/${placeId}/`);
  return response.data;
};

export const createPlace = async (placeData) => {
  const response = await api.post('/places/', placeData);
  return response.data;
};

export const updatePlace = async (placeId, placeData) => {
  const response = await api.put(`/places/${placeId}/`, placeData);
  return response.data;
};

export const deletePlace = async (placeId) => {
  await api.delete(`/places/${placeId}/`);
  return true;
};

export const addReview = async (placeId, reviewData) => {
  const response = await api.post(`/places/${placeId}/reviews`, reviewData);
  return response.data;
};

export default api;