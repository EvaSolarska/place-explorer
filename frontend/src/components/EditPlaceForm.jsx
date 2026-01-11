import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getPlaceById, updatePlace } from '../api';
import PlaceForm from './PlaceForm';

const EditPlaceForm = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [initialData, setInitialData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPlace = async () => {
      try {
        const data = await getPlaceById(id);
        setInitialData(data);
      } catch (err) {
        setError('Nie udało się wczytać miejsca');
      } finally {
        setLoading(false);
      }
    };
    fetchPlace();
  }, [id]);

  const handleSubmit = async (data) => {
    try {
      await updatePlace(id, data);
      navigate(`/places/${id}`);
    } catch (err) {
      console.error('Błąd aktualizacji:', err);
      alert('Nie udało się zapisać zmian.');
    }
  };

  if (loading) return <div className="text-center p-12">Wczytywanie...</div>;
  if (error) return <div className="text-red-600 text-center p-12">{error}</div>;

  return (
    <PlaceForm
      initialData={initialData}
      onSubmit={handleSubmit}
      title="Edytuj miejsce"
      submitText="Zapisz zmiany"
      isEdit={true}
    />
  );
};

export default EditPlaceForm;