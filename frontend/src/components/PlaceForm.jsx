import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const PlaceForm = ({
  initialData = {},
  onSubmit,
  isEdit = false,
  title,
  submitText
}) => {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    name: '',
    description: '',
    street_address: '',
    city: '',
    country: '',
    visit_duration: '',
    is_free: false,
    ...initialData,
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    const finalValue = type === 'checkbox' ? checked : value;
    setFormData(prev => ({ ...prev, [name]: finalValue }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <div className="max-w-4xl mx-auto mb-12">
      <div className="bg-white rounded-3xl shadow-lg border border-slate-100 overflow-hidden">
        <form onSubmit={handleSubmit} className="p-8 md:p-12 relative">
          <button
            type="button"
            onClick={() => navigate(-1)}
            className="absolute top-6 right-6 p-2 text-slate-400 hover:text-slate-700 rounded-full hover:bg-slate-100 transition-colors"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>

          <header className="mb-10">
            <h2 className="text-3xl font-bold text-slate-800">{title}</h2>
            <p className="mt-2 text-slate-500">
              {isEdit ? 'Zaktualizuj informacje o lokalizacji' : 'Wypełnij informacje o lokalizacji'}
            </p>
          </header>

          <div className="grid grid-cols-1 md:grid-cols-6 gap-6">
            <div className="md:col-span-4 space-y-6">
              <div className="space-y-2">
                <label className="block text-sm font-medium text-slate-700">
                  Nazwa miejsca *
                </label>
                <input
                  name="name"
                  required
                  value={formData.name || ''}
                  onChange={handleChange}
                  className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="np. Zamek w Malborku"
                />
              </div>

              <div className="space-y-2">
                <label className="block text-sm font-medium text-slate-700">Opis</label>
                <textarea
                  name="description"
                  rows={4}
                  value={formData.description || ''}
                  onChange={handleChange}
                  className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                  placeholder="Co sprawia, że to miejsce jest wyjątkowe?"
                />
              </div>
            </div>

            <div className="md:col-span-2 space-y-6">
              <div className="space-y-2">
                <label className="block text-sm font-medium text-slate-700">Miasto</label>
                <input
                  name="city"
                  value={formData.city || ''}
                  onChange={handleChange}
                  className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="np. Kraków"
                />
              </div>

              <div className="space-y-2">
                <label className="block text-sm font-medium text-slate-700">Kraj</label>
                <input
                  name="country"
                  value={formData.country || ''}
                  onChange={handleChange}
                  className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Polska"
                />
              </div>

              <div className="space-y-2">
                <label className="block text-sm font-medium text-slate-700">
                  Czas zwiedzania
                </label>
                <input
                  name="visit_duration"
                  value={formData.visit_duration || ''}
                  onChange={handleChange}
                  className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="ok. 3-4h"
                />
              </div>
            </div>

            <div className="md:col-span-6 space-y-6 pt-6 border-t border-slate-100">
              <div className="space-y-2">
                <label className="block text-sm font-medium text-slate-700">Adres</label>
                <input
                  name="street_address"
                  value={formData.street_address || ''}
                  onChange={handleChange}
                  className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="ul. Główna 12"
                />
              </div>
            </div>
          </div>

          <div className="mt-10 flex flex-col sm:flex-row items-center justify-between gap-6">
            <label className="flex items-center gap-3 cursor-pointer">
              <input
                type="checkbox"
                name="is_free"
                checked={formData.is_free}
                onChange={handleChange}
                className="w-5 h-5 text-blue-600 rounded border-slate-300 focus:ring-blue-500"
              />
              <span className="text-slate-700 font-medium">Wstęp darmowy</span>
            </label>

            <button
              type="submit"
              className={`px-10 py-4 text-white font-semibold rounded-xl shadow-md hover:shadow-lg active:scale-98 transition-colors ${
                isEdit ? 'bg-amber-600 hover:bg-amber-700' : 'bg-blue-600 hover:bg-blue-700'
              }`}
            >
              {submitText}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default PlaceForm;