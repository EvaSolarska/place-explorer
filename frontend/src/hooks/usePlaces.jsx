import { useState, useEffect } from 'react';
import { getAllPlaces } from '../api';

export const usePlaces = () => {
  const [places, setPlaces] = useState([]);

  const fetchPlaces = async () => {
    try {
      const data = await getAllPlaces();
      setPlaces(data);
    } catch (error) {
      console.error('Błąd pobierania listy miejsc:', error);
    }
  };

  useEffect(() => {
    fetchPlaces();
  }, []);

  return { places, fetchPlaces };
};
