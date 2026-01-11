import { createPlace } from '../api';
import PlaceForm from './PlaceForm';

const AddPlaceForm = ({ onPlaceAdded }) => {
  const handleSubmit = async (data) => {
    try {
      await createPlace(data);
      if (onPlaceAdded) onPlaceAdded();
    } catch (err) {
      console.error('Błąd dodawania:', err);
      alert('Nie udało się dodać miejsca.');
    }
  };

  return (
    <PlaceForm
      onSubmit={handleSubmit}
      title="Dodaj nowe miejsce"
      submitText="Dodaj miejsce"
      isEdit={false}
    />
  );
};

export default AddPlaceForm;