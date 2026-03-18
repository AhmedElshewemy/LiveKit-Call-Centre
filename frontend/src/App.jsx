import { useState } from 'react'
import './App.css'
import LiveKitModal from './components/LiveKitModal';

function App() {
  const [showSupport, setShowSupport] = useState(false);

  const handleSupportClick = () => {
    setShowSupport(true)
  }

  return (
    <div className="app">
      <header className="header">
        <div className="logo">SeafoodPro</div>
      </header>

      <main>
        <section className="hero">
          <h1>Premium Seafood Products. Fresh Delivery</h1>
          <p>Same Day Delivery on Orders Over $50</p>
          <div className="search-bar">
            <input type="text" placeholder='Enter product ID or seafood type'></input>
            <button>Search</button>
          </div>
        </section>

        <button className="support-button" onClick={handleSupportClick}>
          Talk to an Agent!
        </button>
      </main>

      {showSupport && <LiveKitModal setShowSupport={setShowSupport}/>}
    </div>
  )
}

export default App
