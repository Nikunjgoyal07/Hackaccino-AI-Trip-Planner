import { useState } from "react";
import ReactMarkdown from "react-markdown";
import Head from "next/head";
import Image from "next/image";

export default function Home() {
  const [formData, setFormData] = useState({
    fromCity: "",
    toCity: "",
    dateFrom: "",
    dateTo: "",
    interests: "",
    budget: "",
  });

  const [responseSections, setResponseSections] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const calculateDays = (start, end) => {
    const from = new Date(start);
    const to = new Date(end);
    const diffTime = Math.abs(to - from);
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  };

  const addSection = (text) => {
    setResponseSections((prev) => [...prev, text]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResponseSections([]);

    try {
      const { fromCity, toCity, dateFrom, dateTo, interests, budget } = formData;
      const num_days = calculateDays(dateFrom, dateTo);

      // Top Places
      const placesRes = await fetch(`https://api.wizerservices.com/getplaces?destination_city=${toCity}`);
      const placesData = await placesRes.json();
      const formattedPlaces = placesData.list_of_places
        .map((place, idx) => `**${idx + 1}. ${place.name}**\n${place.description}`)
        .join("\n\n");
      addSection(`**Places to Visit in ${toCity}**\n\n${formattedPlaces}`);

      // Recommendations
      const recUrl = `https://api.wizerservices.com/getreccomendations?from_city=${fromCity}&destination_city=${toCity}&num_days=${num_days}&interests=${interests}&max_budget=${budget}`;
      const recRes = await fetch(recUrl);
      const recData = await recRes.json();

      const formattedRecommendation = `
**Trip Recommendations**

**Travel Mode:** ${recData.travel_mode || "Not available"}  
**Hotel Type:** ${recData.hotel_type || "Not available"}  
**Best Location to Stay:** ${recData.location_details || "Not available"}  
**Food Recommendations:** ${recData.food_recommendation || "Not available"}  
**Must-Visit Places & Activities:** ${recData.activities_recommendation || "Not available"}
`;
      addSection(formattedRecommendation);

      // Activities
      const actRes = await fetch(`https://api.wizerservices.com/getactivities?destination_city=${toCity}`);
      const actData = await actRes.json();
      const formattedActivities = actData.list_of_activities
        .map((activity, idx) => `**${idx + 1}. ${activity.name}**\n${activity.description}`)
        .join("\n\n");
      addSection(`**Activities in ${toCity}**\n\n${formattedActivities}`);

      // Fine Dining / Cafes
      const diningType = budget > 30000 ? "fineDining" : "cafes";
      const diningLabel = budget > 30000 ? "Fine Dining Restaurants" : "Cafes";
      const diningRes = await fetch(`https://api.wizerservices.com/get${diningType}?destination_city=${toCity}`);
      const diningData = await diningRes.json();
      const listKey = budget > 30000 ? "list_of_fine_dining" : "list_of_cafes";
      const formattedDining = diningData[listKey]
        .map((place, idx) => `**${idx + 1}. ${place.name}**\n${place.description}`)
        .join("\n\n");
      addSection(`**Top 5 ${diningLabel} in ${toCity}**\n\n${formattedDining}`);

      // Street Food
      const streetRes = await fetch(`https://api.wizerservices.com/getstreetfood?destination_city=${toCity}`);
      const streetData = await streetRes.json();
      const formattedStreet = streetData.list_of_street_food
        .map((place, idx) => `**${idx + 1}. ${place.name}**\n${place.description}`)
        .join("\n\n");
      addSection(`**Street Food Spots in ${toCity}**\n\n${formattedStreet}`);
    } catch (err) {
      console.error("Error:", err);
      addSection("❌ An error occurred while fetching data. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Head>
        <title>Trip-AI</title>
      </Head>

      {/* Background Video */}
      <div className="fixed top-0 left-0 w-full h-full z-0">
        <video
          autoPlay
          muted
          loop
          playsInline
          className="w-full h-full object-cover"
        >
          <source src="/background.mp4" type="video/mp4" />
          Your browser does not support the video tag.
        </video>
        <div className="absolute inset-0 bg-black bg-opacity-60" />
      </div>

      {/* Foreground Content */}
      <div className="relative z-10 flex flex-col items-center w-full min-h-screen overflow-x-hidden">
        {/* Navbar */}
        <nav className="w-full sticky top-0 z-20 bg-black/70 backdrop-blur-md py-4 px-6 shadow-md flex justify-between items-center">
          <h1 className="text-2xl font-extrabold text-white">trip-ai</h1>
          <p className="text-sm text-gray-300 hidden sm:block">Smarter Travel, Simplified ✈️</p>
        </nav>

        {/* Form & Response */}
        <main className="flex-grow w-full px-4 sm:px-6 lg:px-12 flex flex-col items-center pb-16">
          <h2 className="text-3xl font-bold text-white mt-10 mb-8 text-center">Plan Your Perfect Trip</h2>

          <form
            onSubmit={handleSubmit}
            className="z-10 w-full max-w-xl bg-black/70 backdrop-blur-md p-8 rounded-2xl shadow-2xl space-y-5 border border-[#2c2c2c]"
          >
            {["fromCity", "toCity", "interests", "budget"].map((field, idx) => (
              <div key={idx} className="flex flex-col gap-2">
                <label className="text-sm font-medium text-gray-300 capitalize">{field.replace(/([A-Z])/g, ' $1')}</label>
                <input
                  type={field === "budget" ? "number" : "text"}
                  name={field}
                  value={formData[field]}
                  onChange={handleChange}
                  placeholder={field === "budget" ? "e.g. 20000" : ""}
                  className="w-full p-3 rounded-lg bg-[#2b2b2b] text-white"
                  required
                />
              </div>
            ))}

            <div className="grid grid-cols-2 gap-4">
              {["dateFrom", "dateTo"].map((field, idx) => (
                <div key={idx} className="flex flex-col gap-2">
                  <label className="text-sm font-medium text-gray-300 capitalize">
                    {field === "dateFrom" ? "Start Date" : "End Date"}
                  </label>
                  <input
                    type="date"
                    name={field}
                    value={formData[field]}
                    onChange={handleChange}
                    className="w-full p-3 rounded-lg bg-[#2b2b2b] text-white"
                    required
                  />
                </div>
              ))}
            </div>

            <button
              type="submit"
              className="w-full bg-gradient-to-r from-purple-500 to-blue-600 hover:from-purple-600 hover:to-blue-700 transition-all duration-300 p-3 rounded-lg font-semibold text-white text-lg"
            >
              {loading ? "Planning..." : "Submit"}
            </button>

            {loading && (
              <div className="mt-3 text-center text-sm text-blue-300 animate-pulse">
                trip-ai is typing<span className="animate-blink">...</span>
              </div>
            )}
          </form>

          {/* Response Section */}
          {responseSections.length > 0 && (
            <div className="mt-10 w-full max-w-4xl space-y-6">
              {responseSections.map((section, idx) => (
                <div key={idx} className="bg-black/80 backdrop-blur-md p-6 rounded-lg shadow-md text-white">
                  {/* <p className="text-green-400 font-bold mb-2">Trip-ai:</p> */}
                  <ReactMarkdown>{section}</ReactMarkdown>
                  {idx !== responseSections.length - 1 && <hr className="mt-6 border-gray-600" />}
                </div>
              ))}
            </div>
          )}
        </main>
      </div>
    </>
  );
}
