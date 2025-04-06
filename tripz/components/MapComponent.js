import { useEffect, useRef } from "react";

const MapComponent = ({ fromCity, toCity }) => {
  const mapRef = useRef(null);

  useEffect(() => {
    if (!fromCity || !toCity || typeof window === "undefined") return;

    const directionsService = new google.maps.DirectionsService();
    const directionsRenderer = new google.maps.DirectionsRenderer();

    const map = new google.maps.Map(mapRef.current, {
      zoom: 6,
      center: { lat: 22.9734, lng: 78.6569 }, // center of India
    });

    directionsRenderer.setMap(map);

    directionsService.route(
      {
        origin: fromCity,
        destination: toCity,
        travelMode: google.maps.TravelMode.TRANSIT,
      },
      (result, status) => {
        if (status === "OK") {
          directionsRenderer.setDirections(result);
        } else {
          console.error("Directions request failed due to " + status);
        }
      }
    );
  }, [fromCity, toCity]);

  return <div ref={mapRef} className="w-full h-full" />;
};

export default MapComponent;
