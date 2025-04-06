import { Html, Head, Main, NextScript } from "next/document";

export default function Document() {
  return (
    <Html lang="en">
      <Head />
      <body className="antialiased">
        <Main />
        <script src={`https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places`}></script>
        <NextScript />
      </body>
    </Html>
  );
}