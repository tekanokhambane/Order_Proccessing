import React from 'react'
import Offcanvas from 'react-bootstrap/Offcanvas';
import Button from 'react-bootstrap/Button';
import ListGroup from 'react-bootstrap/ListGroup';
import { BsTrash } from 'react-icons/bs';
import { useNavigate } from 'react-router-dom';


const Drawer = ({ handleClose, show, cartItems, handleChange, removeItem }) => {
    const navigate = useNavigate();
    const goToCheckout = () => {
        navigate('/checkout');
        handleClose();
    }
    return (
        <div>
            <Offcanvas show={show} onHide={handleClose} placement={"end"} style={{ overflowX: 'hidden' }}>
                <Offcanvas.Header closeButton className='d-flex justify-content-between gap-3'>
                    <Offcanvas.Title>Cart Items</Offcanvas.Title>
                    <Offcanvas.Title>{cartItems.length} items</Offcanvas.Title>
                </Offcanvas.Header>
                <Offcanvas.Body style={{ maxHeight: 'calc(100vh - 150px)', overflowY: 'auto', overflowX: 'hidden' }}>
                    {cartItems.length === 0 && <p className='text-center'>Your cart is empty</p>}
                    {cartItems.length > 0 && <ListGroup as="ul"  >
                        {cartItems.map((item) => (
                            <ListGroup.Item as="li" key={item.product.id} className="d-flex justify-content-between align-items-center gap-3">
                                <div className='w-25'>
                                    <img src={item.product.image} alt={item.product.name} style={{ width: '70px', height: '70px' }} />
                                </div>
                                <div className='w-50  d-flex flex-column align-items-end justify-content-end'>
                                    <h5>{item.product.name}</h5>
                                    <p>${item.product.price}</p>
                                    <p className='d-flex align-items-end justify-content-end gap-2'>Qty: <input type="number" onChange={(e) => handleChange(e, item)} min={1} max={10} defaultValue={item.qty} className='form-control w-50' /></p>
                                </div>
                                <div className='w-25'>
                                    <Button variant="danger" onClick={() => removeItem(item)}>
                                        <BsTrash />
                                    </Button>
                                </div>
                            </ListGroup.Item>
                        ))}
                    </ListGroup>}


                    <div style={{ position: 'absolute', bottom: 0, width: '100%' }} className='d-flex flex-column justify-content-end gap-2 fixed-bottom p-3 bg-white shadow'>
                        <h5>Total: ${cartItems.reduce((acc, cur) => acc + (cur.product.price * cur.qty), 0)}</h5>
                        <div className='w-100 d-flex justify-content-end gap-3'>
                            <Button variant="secondary" onClick={handleClose}>
                                Close
                            </Button>
                            <Button variant="primary" onClick={goToCheckout}>
                                Go to checkout
                            </Button>
                        </div>
                    </div>
                </Offcanvas.Body>

            </Offcanvas>
        </div>
    )
}

export default Drawer