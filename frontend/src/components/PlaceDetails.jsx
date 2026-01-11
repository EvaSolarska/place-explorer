import { useEffect, useState, useCallback } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { getPlaceById, deletePlace, addReview } from '../api';

const PlaceDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  const [place, setPlace] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);

  const [reviewForm, setReviewForm] = useState({
    title: '',
    content: '',
    rating: 5,
  });

  const fetchPlace = useCallback(async () => {
    try {
      setLoading(true);
      const data = await getPlaceById(id);
      setPlace(data);
    } catch (err) {
      setError('Nie udało się załadować szczegółów miejsca');
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => {
    fetchPlace();
  }, [fetchPlace]);

  const handleReviewChange = (e) => {
    const { name, value } = e.target;
    setReviewForm((prev) => ({
      ...prev,
      [name]: name === 'rating' ? Number(value) : value,
    }));
  };

  const handleReviewSubmit = async (e) => {
    e.preventDefault();
    if (isSubmitting) return;

    try {
      setIsSubmitting(true);
      const newReview = await addReview(id, reviewForm);

      setPlace(prev => ({
        ...prev,
        reviews: [newReview, ...(prev.reviews || [])]
      }));

      setReviewForm({ title: '', content: '', rating: 5 });
    } catch (err) {
      console.error('Błąd dodawania recenzji:', err);
      alert('Nie udało się dodać opinii.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm('Czy na pewno chcesz usunąć to miejsce?')) return;

    try {
      await deletePlace(id);
       window.location.href = '/';
    } catch (err) {
      alert('Błąd podczas usuwania.');
    }
  };

  if (loading) return (
    <div className="min-h-[60vh] flex items-center justify-center">
      <div className="animate-pulse text-lg font-medium text-slate-500">Wczytywanie...</div>
    </div>
  );

  if (error || !place) return (
    <div className="max-w-4xl mx-auto mt-12 text-center p-6">
      <div className="bg-red-50 border border-red-200 rounded-2xl p-10 text-red-800">
        <h2 className="text-xl font-bold mb-4">Wystąpił problem</h2>
        <p className="mb-6">{error || 'Nie znaleziono miejsca'}</p>
        <Link to="/" className="px-8 py-3 bg-slate-700 text-white rounded-xl hover:bg-slate-800 transition-all">
          Wróć do listy
        </Link>
      </div>
    </div>
  );

  return (
<div className="max-w-4xl mx-auto p-6 md:p-8">
      <div className="flex flex-wrap items-center justify-between gap-4 mb-8">
        <button
          onClick={() => navigate('/')}
          className="text-slate-600 hover:text-blue-600 flex items-center gap-2 font-medium transition-colors"
        >
          ← Wróć
        </button>

        <div className="flex gap-3">
          <button
            onClick={() => navigate(`/edit/${id}`)}
            className="px-5 py-2 bg-amber-600 text-white rounded-lg hover:bg-amber-700 transition-colors"
          >
            Edytuj
          </button>
          <button
            onClick={handleDelete}
            className="px-5 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
          >
            Usuń
          </button>
        </div>
      </div>

      <div className="bg-white rounded-3xl shadow-lg border border-slate-100 overflow-hidden mb-10">
        <div className="p-8 md:p-10">
          <h1 className="text-3xl md:text-4xl font-bold text-slate-800 mb-3">{place.name}</h1>
          <p className="text-blue-600 font-semibold mb-6">{place.city}, {place.country}</p>
          <p className="text-slate-700 leading-relaxed mb-8 text-lg">{place.description}</p>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 pt-6 border-t border-slate-100 text-sm">
            <InfoItem label="Adres" value={place.street_address} />
            <InfoItem label="Czas zwiedzania" value={place.visit_duration} />
            <InfoItem label="Wstęp" value={place.is_free ? 'Darmowy' : 'Płatny'} />
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <section>
          <h2 className="text-2xl font-bold text-slate-800 mb-6">
            Opinie ({place.reviews?.length || 0})
          </h2>
          <div className="space-y-5">
            {place.reviews?.map((review) => (
              <div key={review.id || review.title} className="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm">
                <div className="flex justify-between items-start mb-2">
                  <h4 className="font-semibold text-slate-800">{review.title}</h4>
                  <div className="text-amber-500">{'★'.repeat(review.rating)}</div>
                </div>
                <p className="text-slate-600 text-sm">{review.content}</p>
              </div>
            ))}
            {!place.reviews?.length && (
              <div className="bg-slate-50 rounded-2xl p-8 text-center text-slate-500">
                Brak opinii. Bądź pierwszy!
              </div>
            )}
          </div>
        </section>

        <aside className="lg:sticky lg:top-8 h-fit">
          <div className="bg-slate-900 text-white rounded-3xl p-8 shadow-xl">
            <h3 className="text-xl font-bold mb-6">Dodaj swoją opinię</h3>
            <form onSubmit={handleReviewSubmit} className="space-y-4">
              <input
                name="title"
                placeholder="Tytuł"
                required
                value={reviewForm.title}
                onChange={handleReviewChange}
                disabled={isSubmitting}
                className="w-full bg-white/10 border border-white/20 rounded-xl px-4 py-3 focus:ring-2 focus:ring-blue-500 outline-none"
              />
              <select
                name="rating"
                value={reviewForm.rating}
                onChange={handleReviewChange}
                disabled={isSubmitting}
                className="w-full bg-slate-800 border border-white/20 rounded-xl px-4 py-3 outline-none"
              >
                {[5, 4, 3, 2, 1].map(n => <option key={n} value={n}>{n} gwiazdek</option>)}
              </select>
              <textarea
                name="content"
                placeholder="Twoja opinia..."
                required
                rows={4}
                value={reviewForm.content}
                onChange={handleReviewChange}
                disabled={isSubmitting}
                className="w-full bg-white/10 border border-white/20 rounded-xl px-4 py-3 focus:ring-2 focus:ring-blue-500 outline-none resize-none"
              />
              <button
                type="submit"
                disabled={isSubmitting}
                className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-slate-600 py-3.5 rounded-xl font-semibold transition-all"
              >
                {isSubmitting ? 'Wysyłanie...' : 'Wyślij opinię'}
              </button>
            </form>
          </div>
        </aside>
      </div>
    </div>
  );
};

const InfoItem = ({ label, value }) => (
  <div>
    <span className="block text-slate-500 mb-1">{label}</span>
    <div className="font-medium">{value || '—'}</div>
  </div>
);

export default PlaceDetails;