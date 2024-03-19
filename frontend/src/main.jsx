import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'
import { PayPalScriptProvider } from "@paypal/react-paypal-js";

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    {/* <PayPalScriptProvider
      options={{
        "client-id": "AVCqUVw4MjYOeckkDC0VO0VvgsuxaOEJ9EzYQnnKScuZokUKX8U7z11Fd2k9fidK23vhyCS44Q1cjuE-",
        intent: "capture",
        currency: "USD",
        buyerCountry: "ZA",
        components: "buttons",
        crossorigin: "anonymous"
    </PayPalScriptProvider>
      }}> */}
    <App />
  </React.StrictMode>,
)
