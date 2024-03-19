import { useEffect, useRef, useState } from 'react'
import './App.css'
import 'bootstrap/dist/css/bootstrap.min.css';
import { Container } from 'react-bootstrap';
import NavbarItem from './components/Navbar'
import Home from './pages/Home';
import Login from './pages/Login';
import Drawer from './components/Drawer';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Checkout from './pages/Checkout';
import axios from 'axios';

function App() {
  const [cartItems, setCartItems] = useState([]);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [user, setUser] = useState(null);
  let listItems = useRef(JSON.parse(localStorage.getItem('cartItems')) || []);

  useEffect(() => {
    axios.get('/auth/user').then((res) => {
      if (res.data) {
        setUser(res.data.user);
        console.log(res.data.user);
      }
    }).catch((err) => {
      console.log(err);
    })
  }, []);


  const toggleDrawer = () => {
    setDrawerOpen(!drawerOpen);
  }

  const handleChange = (event, item) => {
    listItems.current.forEach((i) => {
      if (i.product.id === item.product.id) {
        i.qty = parseInt(event.target.value);
      }
    })
    setCartItems([...listItems.current]);
  }

  const removeItem = (item) => {
    listItems.current = listItems.current.filter((i) => i.product.id !== item.product.id);
    setCartItems([...listItems.current]);
  }

  // Load cart items from localStorage on component mount
  useEffect(() => {
    if (localStorage.getItem('cartItems')) {
      if (listItems.current.length > 0) {
        setCartItems([...listItems.current]);
      }

    }
  }, []);

  // Update localStorage whenever cartItems change
  useEffect(() => {
    localStorage.setItem('cartItems', JSON.stringify(cartItems));
  }, [cartItems, listItems]);

  const addToCart = (product) => {
    //check if product is already in cart
    if (listItems.current.find((item) => item.product.id === product.id)) {
      listItems.current.forEach((item) => {
        if (item.product.id === product.id) {
          item.qty++;
          setCartItems([...listItems.current]);
        }
      })
    } else {
      listItems.current.push({ product, qty: 1 });
      setCartItems([...listItems.current]);
    }
  };


  return (
    <div style={{ height: '100vh', width: '100vw' }}>
      <BrowserRouter>
        <Container fluid>
          <NavbarItem cartItems={cartItems} toggleDrawer={toggleDrawer} />
          <Routes>
            <Route path="/" element={<Home addToCart={addToCart} />} />
            <Route path="/checkout" element={<Checkout setCartItems={setCartItems} cartItems={cartItems} />} />
            <Route path="/login" element={<Login />} />
          </Routes>

        </Container>
        <Drawer cartItems={cartItems} show={drawerOpen} removeItem={removeItem} handleChange={handleChange} handleClose={toggleDrawer} />
      </BrowserRouter>
    </div>
  )
}

export default App
