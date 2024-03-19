import { Container } from 'react-bootstrap'
import { useNavigate } from 'react-router-dom'



const Checkout = ({ cartItems, setCartItems }) => {
    const navigate = useNavigate();

    const createOrderItem = async (order, product, qty) => {
        return await fetch("/api/orderitems/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            // use the "body" param to optionally pass additional order information
            // like product skus and quantities
            body: JSON.stringify({
                order: order,
                product: product,
                qty: qty
            }),
        })
            .then((response) => response.json())
            .then((orderItem) => {
                console.log(orderItem, orderItem.id)
            }
            ).catch((error) => {
                console.log(error);
            });
    }

    const createOrder = async () => {
        // Order is created on the server and the order id is returned
        return await fetch("/api/orders/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            // use the "body" param to optionally pass additional order information
            // like product skus and quantities
            body: JSON.stringify({
                status: 'created',

            }),
        })
            .then((response) => response.json())
            .then((order) => {
                console.log(order, order.id)
                cartItems.forEach((item) => {
                    createOrderItem({
                        order: Number(order.id),
                        product: item.product.id,
                        quantity: item.qty
                    })
                })
            }
            ).catch((error) => {
                console.log(error);
            }).finally(() => {
                navigate('/')
                setCartItems([])
            });
    };



    return (
        <div className='d-flex flex-column w-100 ' style={{ overflowX: 'hidden' }}>

            <h1>Checkout</h1>
            {cartItems.length > 0 && <Container style={{ maxWidth: '500px' }}>
                <div className='d-flex flex-column'>
                    <h4>Order Summary</h4>
                    {cartItems.map((item) => (
                        <div key={item.product.id} className='d-flex justify-content-between align-items-center'>
                            <img src={item.product.image} alt={item.product.name} style={{ width: '50px', height: '50px' }} />
                            <p>{item.product.name} x{item.qty}</p>
                            <p>${item.product.price}</p>
                        </div>
                    ))}
                    <div className='d-flex justify-content-between align-items-center'>
                        <p className='fw-bold'>Total</p>
                        <p className='fw-bold'>${cartItems.reduce((acc, cur) => acc + (cur.product.price * cur.qty), 0)}</p>
                    </div>
                </div>
                {/* button for checkout */}
                <div className='d-flex justify-content-center'>
                    <button onClick={createOrder} className='btn btn-info text-white shadow'> Checkout</button>
                </div>
            </Container>}
            {cartItems.length === 0 &&
                <Container style={{ maxWidth: '500px', textAlign: 'center' }}><h3 className='text-center'>Your cart is empty</h3><p>Please add items to your cart, then proceed to checkout</p></Container>
            }
        </div>
    )
}

export default Checkout