import React, { useState } from 'react';
import { fetchPropertyDetails } from './services/property';

const App: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [apiResponse, setApiResponse] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [buttonSearchEnabled, setButtonSearchEnabled] = useState(false);
  const backendApiUrl = import.meta.env.VITE_BACKEND_API_URL;

  const handleSearch = async () => {
    if (loading) return;  // Avoid searching while other search is in progress
    setLoading(true);
    setButtonSearchEnabled(false);

    try {
      const data = await fetchPropertyDetails(backendApiUrl, searchTerm);
      setApiResponse(data);
    } catch (error) {
      setApiResponse({ error: 'Failed to fetch data' });
    } finally {
      setLoading(false);
      setButtonSearchEnabled(true);
    }
  };

  const handleKeyUp = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && searchTerm) {
      handleSearch();
      return;
    }
    setButtonSearchEnabled(searchTerm != "" && !loading);
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">Hometap Property Detail Search</h1>
      <div className="flex items-center space-x-4 mb-4">
        <input
          type="text"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          onKeyUp={handleKeyUp}
          placeholder="Enter full address, including street, city, state, and zip"
          className="p-3 border border-gray-300 rounded-md w-[600px]"
        />
        <button
          onClick={handleSearch}
          disabled={!buttonSearchEnabled}
          className={`bg-blue-500 text-white px-6 py-3 rounded-md ${
            buttonSearchEnabled
              ? 'hover:bg-blue-600 cursor-pointer'
              : 'opacity-50 cursor-not-allowed'
          }`}
        >
          Search
        </button>
      </div>
      {apiResponse && apiResponse.error && (
        <div className="mt-6 bg-red-100 text-red-800 p-4 rounded-md w-full max-w-xl text-left">
          <p>{apiResponse.error}</p>
        </div>
      )}

      {apiResponse && !apiResponse.error && (
        <div className="mt-6 w-full max-w-xl">            
          <div className="bg-white shadow-md rounded-md p-6">
            
            <div className="space-y-2">
              <div className="flex justify-center">
                <h2 className="text-2xl font-bold text-gray-800 mb-4">{apiResponse.normalized_address}</h2>
              </div>
              
              <div className="flex justify-between mb-6">
                <div className="text-xl text-gray-800"><u>Property type:</u> <b>{apiResponse.property_type}</b></div>
                <div className="text-xl font-bold text-blue-800">$ {apiResponse.sale_price.toLocaleString()}</div>
              </div>

              <div className="text-xl text-gray-800 mb-6"><u>Built in:</u> {apiResponse.year_built}</div>

              <div className="flex justify-between items-center">
                <div className="font-medium text-gray-800"><u>Lot Size:</u> <b>{apiResponse.lot_size_acres} acres</b></div>
                <div className="font-medium text-gray-800"><u>Bedrooms:</u> <b>{apiResponse.bedrooms}</b></div>
              </div>

              <div className="flex justify-between items-center">
                <div className="font-medium text-gray-800"><u>Square Footage:</u> <b>{apiResponse.square_footage}</b></div>
                <div className="font-medium text-gray-800"><u>Bathrooms:</u> <b>{apiResponse.bathrooms}</b></div>
              </div>

              <div className="flex justify-between items-center">
                <div className="font-medium text-gray-800"><u>Septic System:</u> <b className={apiResponse.septic_system ? "text-green-500" : "text-black-500"}>
                  {apiResponse.septic_system ? "Yes" : "No"}
                </b>
                </div>
                <div className="font-medium text-gray-800"><u>Rooms:</u> <b>{apiResponse.room_count}</b></div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default App;
