import { Routes, Route, useNavigate, Link } from 'react-router-dom';
import { useEffect, useState } from 'react';
import axios from 'axios';
import AddPlaceForm from './components/AddPlaceForm';
import PlaceDetails from './components/PlaceDetails';
import EditPlaceForm from './components/EditPlaceForm'
import ServerStatusBar from './components/ServerStatusBar'
import { getAllPlaces } from './api';
import { usePlaces } from './hooks/usePlaces';
import { useServerStatus } from './hooks/useServerStatus';

function App() {

  const { places, fetchPlaces } = usePlaces();
  const serverStatus = useServerStatus();
  const navigate = useNavigate();

 return (
    <div className="min-h-screen bg-slate-50">
      <ServerStatusBar status={serverStatus} />
      <Routes>
        <Route
          path="/"
          element={
            <div className="max-w-6xl mx-auto p-8">
              <header className="flex justify-between items-center mb-12">
                <h1 className="text-4xl font-black text-slate-800">PlaceExplorer 🌍</h1>
                <Link
                  to="/add"
                  className="bg-blue-600 text-white px-8 py-3 rounded-2xl font-bold shadow-lg hover:shadow-blue-200 transition"
                >
                  + Dodaj Miejsce
                </Link>
              </header>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                {places.map(place => (
                  <Link to={`/places/${place.id}`} key={place.id} className="group">
                    <div className="bg-white p-8 rounded-[2.5rem] shadow-sm hover:shadow-xl transition-all relative">
                      <h3 className="font-black text-2xl text-slate-800 pr-24 group-hover:text-blue-600 transition-colors">
                        {place.name}
                      </h3>
                      <p className="text-blue-500 text-xs font-black uppercase mt-1 tracking-widest">
                        {place.city}
                      </p>
                      <p className="mt-4 text-slate-500 line-clamp-2 text-sm italic">
                        "{place.description}"
                      </p>
                    </div>
                  </Link>
                ))}
              </div>
            </div>
          }
        />
        <Route path="/places/:id" element={<PlaceDetails />} />
        <Route
          path="/add"
          element={
            <AddPlaceForm
              onPlaceAdded={() => {
                fetchPlaces();
                navigate('/');
              }}
            />
          }
        />
        <Route path="/edit/:id" element={<EditPlaceForm />} />
      </Routes>
    </div>
  );
}


export default App;