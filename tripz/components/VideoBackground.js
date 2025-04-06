export default function VideoBackground() {
    return (
      <div className="fixed inset-0 w-full h-full z-0">
        <video
          autoPlay
          muted
          loop
          playsInline
          className="absolute top-0 left-0 w-full h-full object-cover"
        >
          <source src="/background.mp4" type="video/mp4" />
          Your browser does not support the video tag.
        </video>
        {/* Optional dark overlay for contrast */}
        <div className="absolute top-0 left-0 w-full h-full bg-black bg-opacity-50" />
      </div>
    );
  }
  